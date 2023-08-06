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

from __future__ import annotations

import os
import random
import string
from typing import Optional as Nullable

import yaml
from schema import Optional
from schema import Or
from schema import Schema
from schema import SchemaError
from schema import Use

from bosun.plugin.azureml.config.config_keys import EndpointType
from bosun.plugin.azureml.config.config_keys import Key
from bosun.plugin.deployment_info import DeploymentInfo
from bosun.plugin.pe_info import PEInfo

AZURE_BASE_ENVIRONMENT = (
    "mcr.microsoft.com/azureml/minimal-ubuntu20.04-py38-cpu-inference:20230313.v1"
)
AZURE_CUSTOM_ENVIRONMENT = "datarobot-scoring-code"
AZURE_TEMPLATE_DIR = os.environ.get("BOSUN_AZURE_TEMPLATE_DIR", "/override/templates/")


def output_action_validator(value):
    allowed_values = {"AppendRow", "SummaryOnly"}
    parts = value.split(" ")
    result = "".join(part.capitalize() for part in parts)
    if result not in allowed_values:
        raise SchemaError(None, errors=f"Output action allowed values: [{allowed_values}]")
    return result


class EndpointConfig:
    # besides of type validation, converts numeric string to int
    optional_int_type = Or(None, Use(int), int)

    base_config_schema = {
        Key.AZURE_CLIENT_ID.name: str,
        Key.AZURE_CLIENT_SECRET.name: str,
        Key.AZURE_TENANT_ID.name: str,
        # required subscription/workspace keys
        Key.AZURE_SUBSCRIPTION_ID.name: str,
        Key.AZURE_RESOURCE_GROUP.name: str,
        Key.AZURE_WORKSPACE.name: str,
        Key.AZURE_LOCATION.name: str,
        # optional
        Optional(Key.AZURE_ENVIRONMENT_NAME.name, default=AZURE_CUSTOM_ENVIRONMENT): Or(None, str),
        Optional(Key.AZURE_ENVIRONMENT_LABEL.name, default="latest"): Or(None, str),
        Optional(Key.AZURE_ENVIRONMENT_TAGS.name, default={}): Or(None, dict),
        Optional(Key.LOGGING_LEVEL.name, default="info"): Or(None, str),
        Optional(Key.DEPLOYMENT_LOG_LINES_COUNT.name, default=100): optional_int_type,
        Optional(Key.SCORING_TIMEOUT_SECONDS.name, default=60): optional_int_type,
        Optional(Key.ENDPOINT_DEPLOYMENT_TIMEOUT.name, default=600): optional_int_type,
        Optional(Key.ENDPOINT_DELETION_TIMEOUT.name, default=600): optional_int_type,
        Optional(Key.DEPLOYMENT_DELETION_TIMEOUT.name, default=600): optional_int_type,
        Optional(Key.ENDPOINT_CREATION_TIMEOUT.name, default=600): optional_int_type,
        Optional(Key.AZURE_LOCAL_TESTING.name, default=False): bool,
    }

    online_endpoint_schema = {
        **base_config_schema,
        Key.ENDPOINT_NAME.name: str,
        Key.DEPLOYMENT_NAME.name: str,
        Key.COMPUTE_VIRTUAL_MACHINE.name: str,
        # TODO AGENT-4108 UI should store endpoint type in Deployment's additional metadata
        Optional(Key._ENDPOINT_TYPE.name): Or(None, "online"),
        Optional(Key.COMPUTE_INSTANCE_COUNT.name, default=1): optional_int_type,
        Optional(Key.DEPLOYMENT_TRAFFIC_TIMEOUT.name, default=600): optional_int_type,
    }

    batch_endpoint_schema = {
        **base_config_schema,
        Key.ENDPOINT_NAME.name: str,
        Key.DEPLOYMENT_NAME.name: str,
        Key.COMPUTE_CLUSTER.name: str,
        Key.COMPUTE_CLUSTER_INSTANCE_COUNT.name: Use(int),
        # TODO AGENT-4108 UI should store endpoint type in Deployment's additional metadata
        Optional(Key._ENDPOINT_TYPE.name): Or(None, "batch"),
        Optional(Key.OUTPUT_ACTION.name, default="AppendRow"): Or(
            None, Use(output_action_validator)
        ),
        Optional(Key.OUTPUT_FILE_NAME.name, default="predictions.csv"): Or(None, str),
        Optional(Key.MINI_BATCH_SIZE.name, default=10): optional_int_type,
        Optional(Key.MAX_RETRIES.name, default=3): optional_int_type,
        Optional(Key.MAX_CONCURRENCY_PER_INSTANCE.name, default=1): optional_int_type,
        Optional(Key.ERROR_THRESHOLD.name, default=-1): optional_int_type,
        Optional(Key.AZURE_LOCAL_TESTING.name, default=False): False,  # batch doesn't support local
    }

    configs = {
        EndpointType.ONLINE_ENDPOINT: Schema(online_endpoint_schema, ignore_extra_keys=True),
        EndpointType.BATCH_ENDPOINT: Schema(batch_endpoint_schema, ignore_extra_keys=True),
        EndpointType.DEFAULT: Schema(base_config_schema, ignore_extra_keys=True),
    }

    def __init__(
        self,
        plugin_config: dict,
        endpoint_type: EndpointType = None,
        prediction_environment=None,
        deployment=None,
    ):
        self._config = plugin_config
        self._endpoint_type = endpoint_type
        self.prediction_environment = prediction_environment
        self.deployment = deployment

    def __getitem__(self, key: Key):
        return self._config.get(key.name)

    def validate_config(self):
        schema = self.configs[self.deduce_endpoint_type_by_config()]
        self._config = schema.validate(self._config)

    @classmethod
    def read_config(
        cls,
        config_file_path: Nullable[str] = None,
        endpoint_type: EndpointType = None,
        prediction_environment: PEInfo = None,
        deployment: Nullable[DeploymentInfo] = None,
    ) -> EndpointConfig:
        def get_kv_config(entity):
            result = {}
            if entity.kv_config:
                for key in Key.all():
                    if key in entity.kv_config:
                        result[key] = entity.kv_config[key]
            return result

        config = {}
        if config_file_path:
            with open(config_file_path) as conf_file:
                config = yaml.safe_load(conf_file)

        # override configuration with env variables
        for key in Key.all():
            if key in os.environ:
                config[key] = os.environ[key]

        if prediction_environment:
            pe_additional_metadata = get_kv_config(prediction_environment)
            config.update(pe_additional_metadata)

        if deployment:
            deployment_additional_metadata = get_kv_config(deployment)
            config.update(deployment_additional_metadata)

        return EndpointConfig(config, endpoint_type, prediction_environment, deployment)

    def deduce_endpoint_type_by_config(self):
        if self.is_online_endpoint:
            return EndpointType.ONLINE_ENDPOINT
        elif self.is_batch_endpoint:
            return EndpointType.BATCH_ENDPOINT
        else:
            return EndpointType.DEFAULT

    @property
    def endpoint_type(self):
        return self._config.get(Key._ENDPOINT_TYPE.name)

    @property
    def is_online_endpoint(self):
        if self.endpoint_type:
            return self.endpoint_type == EndpointType.ONLINE_ENDPOINT.value

        online_endpoint_keys = {Key.COMPUTE_VIRTUAL_MACHINE.name, Key.COMPUTE_INSTANCE_COUNT.name}

        return any(key in self._config for key in online_endpoint_keys)

    @property
    def is_batch_endpoint(self):
        if self.endpoint_type:
            return self.endpoint_type == EndpointType.BATCH_ENDPOINT.value

        batch_endpoint_keys = {Key.COMPUTE_CLUSTER.name, Key.COMPUTE_CLUSTER_INSTANCE_COUNT.name}

        return any(key in self._config for key in batch_endpoint_keys)

    def generate_default_name(self):
        postfix_length = 5
        postfix = "".join(random.choice(string.ascii_letters) for x in range(postfix_length))
        workspace_name = self._config.get(Key.AZURE_WORKSPACE)
        return f"{workspace_name}-{postfix}"
