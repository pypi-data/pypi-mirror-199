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
from typing import Optional
from typing import Union

from bosun.plugin.action_status import ActionDataFields
from bosun.plugin.action_status import ActionStatus
from bosun.plugin.action_status import ActionStatusInfo
from bosun.plugin.azureml.azureml_status_reporter import MLOpsStatusReporter
from bosun.plugin.azureml.client.base_endpoint_client import ListOnlyEndpointClient
from bosun.plugin.azureml.client.batch_endpoint_client import BatchEndpointClient
from bosun.plugin.azureml.client.online_endpoint_client import OnlineEndpointClient
from bosun.plugin.azureml.config.azureml_client_config import EndpointConfig
from bosun.plugin.azureml.config.config_keys import EndpointType
from bosun.plugin.bosun_plugin_base import BosunPluginBase
from bosun.plugin.constants import DeploymentState
from bosun.plugin.deployment_info import DeploymentInfo


class AzureMLPlugin(BosunPluginBase):
    AZURE_CLIENTS = {
        EndpointType.ONLINE_ENDPOINT: OnlineEndpointClient,
        EndpointType.BATCH_ENDPOINT: BatchEndpointClient,
        EndpointType.DEFAULT: ListOnlyEndpointClient,
    }

    def __init__(self, plugin_config, private_config_file, pe_info, dry_run):
        super().__init__(plugin_config, private_config_file, pe_info, dry_run)
        http_logger = logging.getLogger("azure.core.pipeline.policies.http_logging_policy")
        http_logger.setLevel(logging.WARNING)

    def get_azure_client(
        self, deployment_info: Optional[DeploymentInfo] = None
    ) -> Union[OnlineEndpointClient, BatchEndpointClient, ListOnlyEndpointClient]:
        assert self._pe_info is not None
        config = EndpointConfig.read_config(
            config_file_path=self._private_config_file,
            prediction_environment=self._pe_info,
            deployment=deployment_info,
        )
        config.validate_config()
        endpoint_type = config.deduce_endpoint_type_by_config()
        self._logger.info("Configuring AzureML client %s...", endpoint_type.name)
        azure_client_cls = self.AZURE_CLIENTS[endpoint_type]
        return azure_client_cls(config)

    def deployment_list(self):
        azure_client = self.get_azure_client()
        datarobot_model_deployments = azure_client.list_deployments()

        status_msg = (
            (f"Found {len(datarobot_model_deployments)} deployment(s)")
            if len(datarobot_model_deployments) > 0
            else "No deployments found"
        )

        self._logger.info(status_msg)

        deployments_map = {
            deployment_id: ActionStatusInfo(ActionStatus.OK, state=deployment_state).__dict__
            for deployment_id, deployment_state in datarobot_model_deployments.items()
        }

        return ActionStatusInfo(ActionStatus.OK, msg=status_msg, data=deployments_map)

    def deployment_start(self, di: DeploymentInfo):
        self._logger.info("Deployment start action invoked for the deployment %s...", di.id)
        if di.model_artifact is None or not di.model_artifact.exists():
            return ActionStatusInfo(
                ActionStatus.ERROR,
                "Model must be pulled from DataRobot deployment, before pushing it to AzureML.",
            )

        try:  # TODO set bosun actionTimeoutWorker timeout to 600-900 seconds
            azure_client = self.get_azure_client(di)
            reporter = MLOpsStatusReporter(self._plugin_config, di, azure_client.ENDPOINT_TYPE)

            reporter.report_deployment("Registering the model...")
            model = azure_client.register_model(di.model_artifact)

            reporter.report_deployment("Creating a new online endpoint...")
            azure_client.create_endpoint()

            reporter.report_deployment(
                "Looking for a custom environment. A new one will be created if does not exist..."
            )
            environment = azure_client.get_latest_environment()

            reporter.report_deployment("Creating a new deployment...")
            azure_client.create_deployment(model, environment)
            # Need to fetch the endpoint after creating the deployment because it
            # seems otherwise it won't always have the scoring_uri filled in.
            endpoint = azure_client.get_endpoint()
            if azure_client.ENDPOINT_TYPE == EndpointType.ONLINE_ENDPOINT:
                reporter.report_deployment("Updating the deployment traffic...")
                azure_client.update_deployment_traffic(new_traffic_value=100)

        except Exception as e:
            self._logger.exception("Failed to start the deployment %s", di.id)
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

        self._logger.info("Scoring code model is successfully deployed to AzureML.")
        status = self.deployment_status(di)
        status.data = {ActionDataFields.PREDICTION_URL: endpoint.scoring_uri}
        return status

    def deployment_relaunch(self, deployment_info: DeploymentInfo):
        # TODO do not re-register model. do not update traffic to 100 if it's already set
        return self.deployment_start(deployment_info)

    def deployment_stop(self, deployment_id: str):
        # TODO 1. check status of each operation
        # TODO 2. send event to DataRobot after each operation
        # TODO 3. if the endpoint is shared then we can't delete it but must delete the deployment
        try:
            azure_client = self.get_azure_client()
            # azure_client.delete_deployment()
            azure_client.delete_endpoint()
            azure_client.delete_model()
        except Exception as e:
            self._logger.exception("Error stopping deployment")
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

        return ActionStatusInfo(ActionStatus.OK, state=DeploymentState.STOPPED)

    def deployment_replace_model(self, deployment_info: DeploymentInfo):
        # TODO: we should do a "blue/green" deployment strategy
        return self.deployment_start(deployment_info)

    def pe_status(self):
        try:
            azure_client = self.get_azure_client()
            azure_client.list_deployments()
            status = ActionStatus.OK
            status_msg = "Azure connection successful"
        except Exception:
            status = ActionStatus.ERROR
            status_msg = "Azure connection failed"
            self._logger.exception(status_msg)

        return ActionStatusInfo(status=status, msg=status_msg)

    def deployment_status(self, deployment_info: DeploymentInfo):
        azure_client = self.get_azure_client(deployment_info)
        try:
            deployment_status = azure_client.deployment_status()
            if deployment_status is None:
                return ActionStatusInfo(ActionStatus.UNKNOWN, state=DeploymentState.STOPPED)

            self._logger.info(
                "Deployment '%s' (%s) has status '%s'",
                deployment_info.name,
                deployment_info.id,
                deployment_status,
            )
            return ActionStatusInfo(ActionStatus.OK, state=deployment_status)
        except Exception as e:
            self._logger.exception("Error checking deployment status")
            return ActionStatusInfo(ActionStatus.ERROR, msg=str(e))

    def plugin_start(self):
        """
        Builds a new Custom environment if one does not exist.
        Azure Custom Environment is expected to be built right after a DataRobot PE is created.
        """
        azure_client = self.get_azure_client()
        azure_client.get_latest_environment()
        return ActionStatusInfo(ActionStatus.OK)

    def plugin_stop(self):
        # NOOP
        return ActionStatusInfo(ActionStatus.OK)
