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

from bosun.plugin.azureml.template_renderer import TemplateRenderer


class AzureMLBatchEndpointScoringSnippet(TemplateRenderer):
    def __init__(self, model_filename: str, csv_separator: str = ","):
        super().__init__()
        self.datarobot_model_filename = model_filename
        self.csv_separator = csv_separator

    def template_name(self) -> str:
        return "azureml_batch_endpoint_score.py"

    def context(self) -> dict:
        return {
            "datarobot_model_filename": self.datarobot_model_filename,
            "csv_separator": self.csv_separator,
        }


class AzureMLOnlineEndpointScoringSnippet(TemplateRenderer):
    def __init__(self, model_filename: str, csv_separator: str = ","):
        super().__init__()
        self.model_filename = model_filename
        self.csv_separator = csv_separator

    def template_name(self) -> str:
        return "azureml_online_endpoint_score.py"

    def context(self) -> dict:
        return {
            "datarobot_model_filename": self.model_filename,
            "csv_separator": self.csv_separator,
        }
