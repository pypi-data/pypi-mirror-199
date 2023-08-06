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
import os
import shutil
from datetime import datetime
from pathlib import Path
from typing import Optional

import pandas as pd
from azureml.contrib.services.aml_request import AMLRequest
from azureml.contrib.services.aml_request import rawhttp
from azureml.contrib.services.aml_response import AMLResponse
from datarobot_predict.scoring_code import ScoringCodeModel
from datarobot_predict.scoring_code import TimeSeriesType
from pydantic import BaseModel
from pydantic import Extra
from pydantic import validator
from pydantic.utils import to_lower_camel

_model = None


# TODO: maybe we could generate this directly from the ScoringCodeModel.predict function
class ScoringCodeModelParams(BaseModel):
    class Config:
        extra = Extra.forbid
        alias_generator = to_lower_camel

    max_explanations: int = 0
    threshold_high: Optional[float] = None
    threshold_low: Optional[float] = None
    time_series_type: TimeSeriesType = TimeSeriesType.FORECAST
    forecast_point: Optional[datetime] = None
    predictions_start_date: Optional[datetime] = None
    predictions_end_date: Optional[datetime] = None
    prediction_intervals_length: Optional[int] = None

    @validator("time_series_type", pre=True)
    def enum_value_or_name(cls, v):
        if isinstance(v, TimeSeriesType):
            return v
        elif isinstance(v, str):
            if v.isdigit():
                return TimeSeriesType(int(v))
            else:
                return TimeSeriesType[v.upper()]
        else:
            return TimeSeriesType(v)


# When running in the VSCode debugger, `JAVA_HOME` isn't being set and is needed
# by `jpype.startJVM()` but we can derive it by looking for the `java` command
# in the PATH.
def _set_java_home():
    if "JAVA_HOME" not in os.environ:
        java_path = shutil.which("java")
        # If we didn't find java, don't raise an error yet and let jpype have
        # a go at it and it will raise an error if it couldn't find it.
        if java_path is not None:
            logging.info("Using path to `java` executable to set JAVA_HOME")
            os.environ["JAVA_HOME"] = str(Path(java_path).parent.parent)


def init():
    global model_path

    _set_java_home()
    model_path = Path(os.environ["AZUREML_MODEL_DIR"]) / os.environ["DATAROBOT_MODEL_FILENAME"]

    # TODO: [AGENT-4189] to work around jpype issues, we can't start the JVM until
    # we are in the worker process (after the fork). For now just do some simple
    # sanity checks.
    if not model_path.exists():
        raise RuntimeError(f"Model JAR is not present: {model_path}")


def _load_model():
    global _model

    if _model is not None:
        logging.info("Found cached model: %s", _model)
    else:
        logging.info("Starting up JVM (JAVA_HOME=%s)", os.environ.get("JAVA_HOME"))
        _model = ScoringCodeModel(str(model_path))
        logging.info(
            "Loaded Model(id=%s; type=%s): %s", _model.model_id, _model.model_type, model_path
        )
    logging.info("Model Info: %s", _model.model_info)
    return _model


@rawhttp
def run(request: AMLRequest):
    model = _load_model()

    if request.method != "POST":
        return AMLResponse("Method not allowed", 405)

    if request.mimetype == "text/csv":
        df = pd.read_csv(request.stream, dtype=model.features)
        params = ScoringCodeModelParams.parse_obj(request.args)

    elif request.mimetype == "application/json":
        if "inputData" not in request.json:
            return AMLResponse('Missing "inputData" field from payload.', 422)
        # To avoid confusion, don't support both query params and params from the JSON payload.
        if request.args:
            return AMLResponse(
                'Query parameters are not supported for "application/json" Content-Type', 422
            )

        inference_data = request.json.pop("inputData")
        df = pd.DataFrame(**inference_data)
        params = ScoringCodeModelParams.parse_obj(request.json)

    else:
        return AMLResponse(
            'Unsupported Content-Type; please use "application/json" or "text/csv"', 422
        )

    results = model.predict(df, **params.dict())
    return results.to_dict(orient="list")
