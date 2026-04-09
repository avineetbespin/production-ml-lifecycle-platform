import mlflow
from mlflow.tracking import MlflowClient

from src.common.config import settings


client = MlflowClient(tracking_uri=settings.MLFLOW_TRACKING_URI)


def register_model(run_id: str, artifact_path: str, model_name: str = settings.MODEL_NAME):
    model_uri = f"runs:/{run_id}/{artifact_path}"
    registered_model = mlflow.register_model(model_uri, model_name)
    return registered_model


def get_stage_model(model_name: str = settings.MODEL_NAME, stage: str = settings.PRODUCTION_STAGE):
    return mlflow.pyfunc.load_model(f"models:/{model_name}/{stage}")


def transition_model_to_production(model_name: str, version: str):
    client.transition_model_version_stage(
        name=model_name,
        version=version,
        stage=settings.PRODUCTION_STAGE,
        archive_existing_versions=True,
    )
    return client.get_model_version(name=model_name, version=version)
