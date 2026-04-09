import argparse

import mlflow
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import train_test_split

from src.common.config import settings
from src.training.benchmark import evaluate_model
from src.training.mldata import build_training_dataset
from src.training.model_registry import register_model


def train_and_register(model_name: str, artifact_path: str):
    dataset = build_training_dataset()
    X = dataset.drop(columns=["target"])
    y = dataset["target"]

    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    with mlflow.start_run() as run:
        model = LogisticRegression(max_iter=500)
        model.fit(X_train, y_train)
        mlflow.sklearn.log_model(model, artifact_path)
        mlflow.log_param("model_type", "LogisticRegression")
        lf = evaluate_model(model, X_test, y_test)
        mlflow.log_metric("accuracy", lf.accuracy)
        mlflow.log_metric("f1_score", lf.f1)
        mlflow.set_tag("stage", "candidate")
        registered_model = register_model(run.info.run_id, artifact_path, model_name)
        print(f"Registered candidate model run_id={run.info.run_id} version={registered_model.version}")
        print(run.info.run_id)
        return run.info.run_id


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Train a candidate model and log it to MLflow.")
    parser.add_argument("--model-name", default=settings.MODEL_NAME)
    parser.add_argument("--artifact-path", default=settings.ARTIFACT_PATH)
    args = parser.parse_args()
    train_and_register(args.model_name, args.artifact_path)
