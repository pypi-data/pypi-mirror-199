# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------

import logging

from typing import Any

import subprocess
import sys
import mlflow

from azure.ai.ml import MLClient
from azure.ai.ml.entities import Workspace
from azure.identity import DefaultAzureCredential

from azureml.rai.utils.constants import (
    AUTOML_MLIMAGES_MLFLOW_MODEL_IDENTIFIER)

_logger = logging.getLogger(__file__)
logging.basicConfig(level=logging.INFO)


def log_info(message):
    _logger.info(message)
    print(message)


class ModelSerializer:
    def __init__(self, model_id: str, ml_client: MLClient,
                 workspace_name: str = None,
                 model_type: str = "pyfunc",
                 use_model_dependency: bool = False,
                 use_conda: bool = True):
        self._model_id = model_id
        self._model_type = model_type
        self._subscription_id = ml_client.subscription_id
        self._resource_group = ml_client.resource_group_name
        self._workspace_name = workspace_name
        self._use_model_dependency = use_model_dependency
        self._use_conda = use_conda

    def save(self, model, path):
        # Nothing to do, since model is saved in AzureML
        pass

    def load(self, path):
        return self.load_mlflow_model(self._model_id)

    def load_mlflow_model(self, model_id: str) -> Any:
        ml_client = MLClient(
            subscription_id=self._subscription_id,
            resource_group_name=self._resource_group,
            workspace_name=self._workspace_name,
            credential=DefaultAzureCredential()
        )
        # set tracking URI
        workspace = ml_client.workspaces.get(name=self._workspace_name)
        tracking_uri = workspace.mlflow_tracking_uri
        mlflow.set_tracking_uri(tracking_uri)

        split_model_id = model_id.rsplit(":", 1)
        model_name = split_model_id[0]
        if model_name == model_id:
            model = ml_client.models.get(model_id, label="latest")
        else:
            version = split_model_id[1]
            model = ml_client.models.get(model_name, version=version)

        model_uri = "models:/{}/{}".format(model.name, model.version)
        if self._use_model_dependency:
            try:
                if self._use_conda:
                    conda_file = mlflow.pyfunc.get_model_dependencies(
                        model_uri, format='conda')
                    log_info("MLFlow model conda file location: {}".format(
                        conda_file))
                    # call conda env update in subprocess
                    subprocess.check_call([sys.executable, "-m", "conda",
                                        "env", "update", "-f", conda_file])
                else:
                    pip_file = mlflow.pyfunc.get_model_dependencies(model_uri)
                    log_info("MLFlow model pip file location: {}".format(
                        pip_file))
                    # call pip install in subprocess
                    subprocess.check_call([sys.executable, "-m", "pip",
                                        "install", "-r", pip_file])
                log_info("Successfully installed model dependencies")
            except Exception as e:
                log_info("Failed to install model dependencies")
                log_info(e)
        else:
            log_info("Skip installing model dependencies")
        if self._model_type == "fastai":
            fastai_model = mlflow.fastai.load_model(model_uri)
            log_info("fastai_model: {0}".format(type(fastai_model)))
            log_info(f"dir(fastai_model): {dir(fastai_model)}")
            return fastai_model
        else:
            mlflow_loaded = mlflow.pyfunc.load_model(model_uri)
            log_info("mlflow_loaded: {0}".format(type(mlflow_loaded)))
            log_info(f"dir(mlflow_loaded): {dir(mlflow_loaded)}")
            if str(type(mlflow_loaded._model_impl.python_model)).endswith(
                AUTOML_MLIMAGES_MLFLOW_MODEL_IDENTIFIER
            ):
                return mlflow_loaded
            model_impl = mlflow_loaded._model_impl
            log_info("model_impl: {0}".format(type(model_impl)))
            log_info(f"dir(model_impl): {dir(model_impl)}")
            internal_model = model_impl.python_model
            log_info(f"internal_model: {type(internal_model)}")
            log_info(f"dir(internal_model): {dir(internal_model)}")
            extracted_model = internal_model._model
            log_info(f"extracted_model: {type(extracted_model)}")
            log_info(f"dir(extracted_model): {dir(extracted_model)}")
            return extracted_model
