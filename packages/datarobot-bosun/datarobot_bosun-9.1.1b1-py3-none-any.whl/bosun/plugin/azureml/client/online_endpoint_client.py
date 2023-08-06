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
from pathlib import Path
from tempfile import TemporaryDirectory
from typing import Union

from azure.ai.ml.constants import AssetTypes
from azure.ai.ml.entities import CodeConfiguration
from azure.ai.ml.entities import Environment
from azure.ai.ml.entities import ManagedOnlineDeployment
from azure.ai.ml.entities import ManagedOnlineEndpoint
from azure.ai.ml.entities import Model
from azure.ai.ml.entities import OnlineDeployment
from azure.ai.ml.entities import OnlineEndpoint
from azure.ai.ml.entities import OnlineRequestSettings
from azure.ai.ml.exceptions import LocalEndpointInFailedStateError
from azure.ai.ml.exceptions import LocalEndpointNotFoundError
from azure.core.exceptions import ResourceNotFoundError

from bosun.plugin.azureml.client.base_endpoint_client import BaseEndpointClient
from bosun.plugin.azureml.client.scoring_snippets import AzureMLOnlineEndpointScoringSnippet
from bosun.plugin.azureml.config.azureml_client_config import AZURE_BASE_ENVIRONMENT
from bosun.plugin.azureml.config.azureml_client_config import EndpointConfig
from bosun.plugin.azureml.config.config_keys import Constants
from bosun.plugin.azureml.config.config_keys import EndpointType
from bosun.plugin.azureml.config.config_keys import Key
from bosun.plugin.azureml.config.config_keys import ProvisioningState


class OnlineEndpointClient(BaseEndpointClient):
    TEMPLATE_DIR = Path(__file__).parent.parent / "templates"
    ENDPOINT_TYPE = EndpointType.ONLINE_ENDPOINT

    def __init__(self, config: EndpointConfig):
        super().__init__(config)
        self.endpoint_name = self.config[Key.ENDPOINT_NAME]
        self.deployment_name = self.config[Key.DEPLOYMENT_NAME]
        self.compute_virtual_machine = self.config[Key.COMPUTE_VIRTUAL_MACHINE]
        self.compute_instance_count = self.config[Key.COMPUTE_INSTANCE_COUNT]

    def get_scoring_snippet(self, model_filename: str) -> str:
        scoring_template = AzureMLOnlineEndpointScoringSnippet(model_filename=model_filename)
        return scoring_template.render()

    def create_endpoint(self):
        endpoint_tags = {
            Key.DATAROBOT_DEPLOYMENT_ID.value: self.datarobot_deployment_id,
            Key.DATAROBOT_ENVIRONMENT_ID.value: self.datarobot_environment_id,
        }
        endpoint_tags.update(self.prediction_environment_tags)
        endpoint = ManagedOnlineEndpoint(
            name=self.endpoint_name, auth_mode=Constants.AUTH_MODE_KEY.value, tags=endpoint_tags
        )

        result = self._client.online_endpoints.begin_create_or_update(endpoint, local=self._local)
        if not self._local:
            result: OnlineEndpoint = result.result(self.config[Key.ENDPOINT_CREATION_TIMEOUT])

        if result.provisioning_state == ProvisioningState.SUCCEEDED.value:
            self.logger.info("Endpoint %s is successfully created.", self.endpoint_name)
        elif self._local:
            # For local, if there was no exception then it was a success
            self.logger.info("Local Endpoint %s is successfully created.", self.endpoint_name)
        else:
            message = (
                f"Failed to create endpoint {endpoint.name}. Status: {result.provisioning_state}"
            )
            self.logger.error(message)
            raise RuntimeError(message)  # TODO should raise custom exception

    def get_endpoint(self) -> OnlineEndpoint:
        return self._client.online_endpoints.get(self.endpoint_name, local=self._local)

    def create_deployment(self, model, environment: Environment):
        model_filename = Path(model.path).name
        scoring_script_name = "score.py"
        deployment_tags = {
            Key.DATAROBOT_ENVIRONMENT_ID.value: self.datarobot_environment_id,
            Key.DATAROBOT_DEPLOYMENT_ID.value: self.datarobot_deployment_id,
            Key.DATAROBOT_MODEL_ID.value: self.datarobot_model_id,
        }
        deployment_tags.update(self.prediction_environment_tags)
        with ScratchDir(cleanup=not self._local) as scoring_code_dir:
            scoring_code_file = scoring_code_dir / scoring_script_name
            scoring_code_file.write_text(self.get_scoring_snippet(model_filename))
            # Fix permissions when running in self._local (e.g. docker bind mount) mode
            scoring_code_dir.chmod(0o755)
            scoring_code_file.chmod(0o644)

            # SDK requires scoring timeout to be in millis
            scoring_timeout_ms = self.config[Key.SCORING_TIMEOUT_SECONDS] * 1000
            deployment = ManagedOnlineDeployment(
                name=self.deployment_name,
                endpoint_name=self.endpoint_name,
                model=model,
                environment=environment,
                code_configuration=CodeConfiguration(
                    code=str(scoring_code_dir), scoring_script=scoring_script_name
                ),
                request_settings=OnlineRequestSettings(request_timeout_ms=scoring_timeout_ms),
                instance_type=self.compute_virtual_machine,
                instance_count=self.compute_instance_count,
                environment_variables={"DATAROBOT_MODEL_FILENAME": str(model_filename)},
                tags=deployment_tags,
            )

            try:
                result = self._client.online_deployments.begin_create_or_update(
                    deployment=deployment, local=self._local
                )
            except LocalEndpointInFailedStateError as e:
                self.logger.error("Failed to create local deployment: %s", e)
                result = type(deployment)(
                    **deployment._to_dict(), provisioning_state=ProvisioningState.FAILED.value
                )

        if not self._local:
            result: OnlineDeployment = result.result(self.config[Key.ENDPOINT_DEPLOYMENT_TIMEOUT])

        if result.provisioning_state == ProvisioningState.SUCCEEDED.value:
            self.logger.info("Deployment %s is successfully created.", self.deployment_name)
        else:
            # TODO should raise custom exception
            msg = (
                f"Failed to create deployment {deployment.name}"
                f" (endpoint={self.endpoint_name};model={model.name})."
                f" Status: {result.provisioning_state}"
            )
            self.logger.error(msg)
            try:
                logs = self._client.online_deployments.get_logs(
                    name=result.name,
                    endpoint_name=result.endpoint_name,
                    lines=60,  # hopefully this is enough context w/o dumping a ton of text
                    local=self._local,
                )
                self.logger.debug("deployment container logs: %s", logs)
                msg += f"\n\nDeployment Logs:\n{logs}"
            except Exception as e:
                self.logger.warning(
                    "Failed to fetch logs for deployment %s (endpoint=%s): %s",
                    result.name,
                    result.endpoint_name,
                    e,
                )
            raise RuntimeError(msg)

        return result

    def delete_endpoint(self):
        self.logger.info("Deleting online endpoint %s...", self.endpoint_name)
        timeout_seconds = self.config[Key.ENDPOINT_DELETION_TIMEOUT]
        try:
            result = self._client.online_endpoints.begin_delete(
                self.endpoint_name, local=self._local
            )
        except LocalEndpointNotFoundError:
            # To be idempotent, if the endpoint is already gone then just ignore.
            pass
        else:
            if not self._local:
                result.result(timeout_seconds)

    def delete_deployment(self):
        self.logger.info(
            "Deleting deployment %s from online endpoint %s...",
            self.deployment_name,
            self.endpoint_name,
        )
        result = self._client.online_deployments.begin_delete(
            name=self.deployment_name, endpoint_name=self.endpoint_name, local=self._local
        )
        if not self._local:
            result.result(self.config[Key.DEPLOYMENT_DELETION_TIMEOUT])

    def deployment_logs(self) -> str:
        return self._client.online_deployments.get_logs(
            name=self.deployment_name,
            endpoint_name=self.endpoint_name,
            lines=self.config[Key.DEPLOYMENT_LOG_LINES_COUNT],
            local=self._local,
        )

    def deployment_status(self) -> Union[None, str]:
        try:
            deployment: OnlineDeployment = self._client.online_deployments.get(
                name=self.deployment_name, endpoint_name=self.endpoint_name, local=self._local
            )
        except (LocalEndpointNotFoundError, ResourceNotFoundError):
            deployment = None

        if deployment is None:
            return None  # status unknown

        return self.map_state(deployment.provisioning_state)

    def update_deployment_traffic(self, await_results=True, new_traffic_value=100):
        endpoint = self._client.online_endpoints.get(self.endpoint_name, local=self._local)
        endpoint.traffic = {self.deployment_name: new_traffic_value}

        result = self._client.online_endpoints.begin_create_or_update(endpoint, local=self._local)

        if await_results and not self._local:
            traffic_update_timeout_seconds = self.config[Key.DEPLOYMENT_TRAFFIC_TIMEOUT]
            result = result.result(traffic_update_timeout_seconds)
            if result.provisioning_state == ProvisioningState.SUCCEEDED.value:
                self.logger.info(
                    "Deployment traffic is updated to 100% for deployment %s.", self.deployment_name
                )
            else:
                # TODO should raise custom exception
                msg = f"Failed to update traffic for the deployment {self.deployment_name}. "
                f"Status: {result.provisioning_state}."
                self.logger.error(msg)
                raise RuntimeError(msg)

    def get_latest_environment(self):
        # Override base method because local mode is only supported for online
        # endpoints currently.
        if self._local:
            return Environment(
                conda_file=self.TEMPLATE_DIR / "conda.yml", image=AZURE_BASE_ENVIRONMENT
            )
        return super().get_latest_environment()

    def register_model(self, model_path):
        if self._local:
            self.logger.info("Skipping local model registration")
            return Model(
                name=self.datarobot_model_name, path=model_path, type=AssetTypes.CUSTOM_MODEL
            )
        return super().register_model(model_path)

    def delete_model(self):
        if self._local:
            self.logger.info("Skipping local model deletion")
            return
        super().delete_model()


class ScratchDir(TemporaryDirectory):
    """
    When running in local mode, AzureML bind mounts the scoring script into the container
    so we can't use an actual temporary file/dir. We will still create the dir/file in
    the temp location so hopefully the OS will cleanup the files for us.
    """

    def __init__(self, cleanup=True, **kwargs):
        super().__init__(**kwargs)
        self._do_cleanup = cleanup
        if not cleanup:
            # If we aren't doing cleanup, detach the finalizer that the parent class sets
            self._finalizer.detach()

    def __enter__(self):
        return Path(self.name)

    def cleanup(self):
        if self._do_cleanup:
            super().cleanup()
