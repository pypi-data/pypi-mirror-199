#  ---------------------------------------------------------------------------------
#  Copyright (c) 2023 DataRobot, Inc. and its affiliates. All rights reserved.
#  Last updated 2023.
#
#  DataRobot, Inc. Confidential.
#  This is proprietary source code of DataRobot, Inc. and its affiliates.
#
#  This file and its contents are subject to DataRobot Tool and Utility Agreement.
#  For details, see
#  https://www.datarobot.com/wp-content/uploads/2021/07/DataRobot-Tool-and-Utility-Agreement.pdf.
#  ---------------------------------------------------------------------------------
import logging
from abc import ABC
from abc import abstractmethod
from pathlib import Path
from typing import Dict
from typing import Union

from azure.ai.ml import MLClient
from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import Endpoint
from azure.ai.ml.entities import Environment
from azure.ai.ml.entities import Model
from azure.core.exceptions import HttpResponseError
from azure.identity import DefaultAzureCredential

from bosun.plugin.azureml.config.azureml_client_config import AZURE_BASE_ENVIRONMENT
from bosun.plugin.azureml.config.azureml_client_config import AZURE_CUSTOM_ENVIRONMENT
from bosun.plugin.azureml.config.azureml_client_config import AZURE_TEMPLATE_DIR
from bosun.plugin.azureml.config.azureml_client_config import EndpointConfig
from bosun.plugin.azureml.config.azureml_client_config import EndpointType
from bosun.plugin.azureml.config.config_keys import Constants
from bosun.plugin.azureml.config.config_keys import Key
from bosun.plugin.azureml.config.config_keys import ProvisioningState
from bosun.plugin.constants import DeploymentState


class BaseEndpointClient(ABC):
    _EXTERNAL_TO_INTERNAL_STATE_MAP = {
        ProvisioningState.FAILED.value: DeploymentState.ERROR,
        ProvisioningState.SUCCEEDED.value: DeploymentState.READY,
        ProvisioningState.DELETING.value: DeploymentState.STOPPED,
        ProvisioningState.CANCELED.value: DeploymentState.STOPPED,
        ProvisioningState.CREATING.value: DeploymentState.LAUNCHING,
        ProvisioningState.SCALING.value: DeploymentState.LAUNCHING,
        ProvisioningState.UPDATING.value: DeploymentState.LAUNCHING,
    }
    ENDPOINT_TYPE = EndpointType.DEFAULT

    def __init__(self, config: EndpointConfig):
        self.logger = logging.getLogger(f"{self.__class__.__module__}.{self.__class__.__name__}")

        self.config = config
        self.environment_name = config[Key.AZURE_ENVIRONMENT_NAME]
        self.environment_label = config[Key.AZURE_ENVIRONMENT_LABEL]
        self.prediction_environment_tags = config[Key.AZURE_ENVIRONMENT_TAGS]
        self.prediction_environment = config.prediction_environment
        self.deployment = config.deployment
        self._client = MLClient(
            DefaultAzureCredential(),
            config[Key.AZURE_SUBSCRIPTION_ID],
            config[Key.AZURE_RESOURCE_GROUP],
            config[Key.AZURE_WORKSPACE],
        )
        self._local: bool = self.config[Key.AZURE_LOCAL_TESTING]

    @property
    def datarobot_environment_id(self):
        return self.prediction_environment.id if self.prediction_environment else None

    @property
    def datarobot_deployment_id(self):
        return self.deployment.id if self.deployment else None

    @property
    def datarobot_model_id(self):
        return (
            (self.deployment.new_model_id or self.deployment.model_id) if self.deployment else None
        )

    @property
    def datarobot_model_name(self):
        # TODO bosun mcrunner should pass model name
        return "dr-" + self.datarobot_model_id if self.datarobot_model_id else None

    @property
    def datarobot_model_description(self):
        # TODO bosun mcrunner should pass model description
        return ""

    def get_latest_environment(self):
        self.logger.info("Looking for environment %s in the registry...", self.environment_name)

        try:
            return self._client.environments.get(
                AZURE_CUSTOM_ENVIRONMENT, label=self.environment_label
            )
        except HttpResponseError:
            self.logger.info("DataRobot scoring environment does not exist. Building a new one.")
            env_docker_image = Environment(
                image=AZURE_BASE_ENVIRONMENT,
                name=AZURE_CUSTOM_ENVIRONMENT,
                description="DataRobot environment containing MLOPS library and wrappers to run "
                "scoring model.",
                conda_file=Path(AZURE_TEMPLATE_DIR) / "conda.yml",
                tags=self.prediction_environment_tags,
            )
            return self._client.environments.create_or_update(env_docker_image)

    def register_model(self, model_path):
        model_tags = {Key.DATAROBOT_MODEL_ID.value: self.datarobot_model_id}
        model_tags.update(self.prediction_environment_tags)

        model = Model(
            name=self.datarobot_model_name,
            path=model_path,
            type=AssetTypes.CUSTOM_MODEL,
            tags=model_tags,
        )
        return self._client.models.create_or_update(model)

    def get_latest_model(self):
        self.logger.info("Looking for model %s in the registry...", self.datarobot_model_id)
        return self._client.models.get(
            self.datarobot_model_name, label=Constants.LATEST_VERSION.value
        )

    def delete_model(self):
        self.logger.info("Deleting DataRobot model %s...", self.datarobot_model_id)
        models = self._client.models.list(self.datarobot_model_name)
        for model in models:
            self._client.models.archive(model.name, model.version)

    @classmethod
    def map_state(cls, provisioning_state):
        return cls._EXTERNAL_TO_INTERNAL_STATE_MAP.get(provisioning_state, DeploymentState.ERROR)

    def list_deployments(self) -> Dict[str, str]:
        self.logger.info(
            "Retrieving list of deployments for prediction environment %s",
            self.prediction_environment.id,
        )
        prediction_environment_deployments = dict()
        for endpoint_type in (EndpointType.ONLINE_ENDPOINT, EndpointType.BATCH_ENDPOINT):
            if endpoint_type == EndpointType.BATCH_ENDPOINT and self._local:
                self.logger.info("Skipping listing batch endpoints when in local mode...")
                continue
            deployments = self._list_deployments_by_type(endpoint_type)
            self.logger.info("Found deployments for %s: %s", endpoint_type, deployments)
            prediction_environment_deployments.update(deployments)
        return prediction_environment_deployments

    def _list_deployments_by_type(self, endpoint_type: EndpointType) -> Dict[str, str]:
        result = dict()
        # Only OnlineEndpoint APIs support the local= kwarg
        is_local = {"local": self._local} if endpoint_type == EndpointType.ONLINE_ENDPOINT else {}
        endpoints_api_client, deployments_api_client = self._get_api_clients(endpoint_type)
        endpoints = endpoints_api_client.list(**is_local)
        for endpoint in endpoints:
            # Multiple PEs can be mapped to a single AzureML workspace so make sure we are only
            # working on endpoints that _this_ PE actually owns.
            tag_value = endpoint.tags.get(Key.DATAROBOT_ENVIRONMENT_ID.value)
            if tag_value is None or tag_value != self.datarobot_environment_id:
                continue

            datarobot_model_deployments = dict()
            deployments = deployments_api_client.list(endpoint_name=endpoint.name, **is_local)
            for deployment in deployments:
                deployment_id = deployment.tags.get(Key.DATAROBOT_DEPLOYMENT_ID.value)
                if deployment_id is None:
                    continue  # skip non DR deployments

                # batch endpoints don't have a provisioning state, thus use an endpoint state
                entity = deployment if EndpointType.ONLINE_ENDPOINT else endpoint
                deployment_state = self.map_state(entity.provisioning_state)
                datarobot_model_deployments[deployment_id] = deployment_state
            result.update(datarobot_model_deployments)
        return result

    def _get_api_clients(self, endpoint_type: EndpointType):
        endpoints_api_client = None
        deployments_api_client = None

        if endpoint_type == EndpointType.ONLINE_ENDPOINT:
            endpoints_api_client = self._client.online_endpoints
            deployments_api_client = self._client.online_deployments
        elif endpoint_type == EndpointType.BATCH_ENDPOINT:
            endpoints_api_client = self._client.batch_endpoints
            deployments_api_client = self._client.batch_deployments

        return endpoints_api_client, deployments_api_client

    def get_scoring_snippet(self, model_filename: str) -> str:
        pass

    @abstractmethod
    def create_endpoint(self):
        pass

    @abstractmethod
    def get_endpoint(self) -> Endpoint:
        pass

    @abstractmethod
    def create_deployment(self, model, environment: Environment):
        pass

    @abstractmethod
    def delete_endpoint(self):
        pass

    @abstractmethod
    def delete_deployment(self):
        pass

    @abstractmethod
    def deployment_status(self) -> Union[None, str]:
        pass

    def check_permissions(self):
        # TODO use active directory to check permissions
        raise NotImplementedError()

    def check_quota(self):
        # TODO use quota rest api
        raise NotImplementedError()


class ListOnlyEndpointClient(BaseEndpointClient):
    def create_endpoint(self) -> Endpoint:
        raise NotImplementedError

    def get_endpoint(self) -> Endpoint:
        raise NotImplementedError

    def create_deployment(self, model):
        raise NotImplementedError

    def delete_endpoint(self):
        raise NotImplementedError

    def delete_deployment(self):
        raise NotImplementedError

    def deployment_status(self) -> Union[None, str]:
        raise NotImplementedError
