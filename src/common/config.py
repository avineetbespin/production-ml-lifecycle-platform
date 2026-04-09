import os

from typing import Optional


class Settings:
    MLFLOW_TRACKING_URI: str = os.getenv("MLFLOW_TRACKING_URI", "http://localhost:5000")
    MODEL_NAME: str = os.getenv("MODEL_NAME", "production-model")
    PRODUCTION_STAGE: str = os.getenv("PRODUCTION_STAGE", "Production")
    PERFORMANCE_THRESHOLD: float = float(os.getenv("PERFORMANCE_THRESHOLD", "0.01"))
    BIAS_THRESHOLD: float = float(os.getenv("BIAS_THRESHOLD", "0.05"))
    DRIFT_THRESHOLD: float = float(os.getenv("DRIFT_THRESHOLD", "0.10"))
    CLOUD_PROVIDER: str = os.getenv("CLOUD_PROVIDER", "gcp")
    ARTIFACT_PATH: str = os.getenv("ARTIFACT_PATH", "model")
    SERVICE_NAME: str = os.getenv("SERVICE_NAME", "ml-model-service")


settings = Settings()
