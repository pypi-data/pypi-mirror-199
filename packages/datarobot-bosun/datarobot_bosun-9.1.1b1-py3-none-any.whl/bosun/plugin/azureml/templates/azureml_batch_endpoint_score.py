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
from pathlib import Path

import pandas as pd
from datarobot_predict.scoring_code import ScoringCodeModel

model_filename = "{{ datarobot_model_filename }}"
_model = None


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
    model_path = Path(os.environ["AZUREML_MODEL_DIR"]) / model_filename

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


def run(mini_batch):
    model = _load_model()

    results = []
    for iteration, file_path in enumerate(mini_batch, start=1):
        try:
            df = pd.read_csv(file_path)
            logging.info("Scoring batch #%s", iteration)
            # TODO: if a batch has an error, should we continue?
            predictions: pd.DataFrame = model.predict(df)
            if predictions.empty:
                logging.warning("Empty results, batch #%s", iteration)
        except Exception:
            # Log the error but continue so we can correctly support the `error_threshold`
            # the user has configured. The AzureML platform does this by monitoring the
            # the gap between mini-batch input count and returns. 'Batch inferencing' scenario
            # should return a list, dataframe, or tuple with the successful items to try to meet
            # this threshold.
            logging.exception(f"Error while processing batch #{iteration}")
            predictions = pd.DataFrame()
        results.append(predictions)
    return pd.concat(results)
