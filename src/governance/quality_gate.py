import argparse
import os

import mlflow
from mlflow.tracking import MlflowClient

from src.common.config import settings
from src.governance.bias import check_bias
from src.governance.drift import create_data_drift_report
from src.training.benchmark import compare_models, evaluate_model
from src.training.mldata import build_training_dataset, load_reference_dataset
from src.training.model_registry import get_stage_model, transition_model_to_production


client = MlflowClient(tracking_uri=settings.MLFLOW_TRACKING_URI)


def get_candidate_model(run_id: str, artifact_path: str):
    return mlflow.pyfunc.load_model(f"runs:/{run_id}/{artifact_path}")


def resolve_reference_data(reference_path: str = None):
    return load_reference_dataset(reference_path)


def run_quality_gate(run_id: str, artifact_path: str, reference_path: str = None):
    champion = get_stage_model()
    candidate = get_candidate_model(run_id, artifact_path)

    benchmark_data = build_training_dataset()
    X_eval = benchmark_data.drop(columns=["target"])
    y_eval = benchmark_data["target"]

    comparison = compare_models(candidate, champion, X_eval, y_eval, settings.PERFORMANCE_THRESHOLD)
    drift_report = create_data_drift_report(benchmark_data, resolve_reference_data(reference_path))
    fairness_result = check_bias(benchmark_data, candidate)

    print("Benchmark comparison:", comparison)
    print("Fairness result:", fairness_result)

    if not comparison["pass_threshold"]:
        raise RuntimeError("Candidate model did not exceed the production baseline.")
    if fairness_result["disparate_impact"] > settings.BIAS_THRESHOLD:
        raise RuntimeError("Bias threshold exceeded for candidate model.")
    if drift_report["data_drift_detected"]:
        raise RuntimeError("Data drift detected relative to production reference distribution.")

    version = _find_candidate_version(run_id)
    transition_model_to_production(settings.MODEL_NAME, version)
    print(f"Promoted model version {version} to Production.")
    return {
        "benchmark": comparison,
        "fairness": fairness_result,
        "drift": drift_report,
    }


def _find_candidate_version(run_id: str) -> str:
    versions = client.search_model_versions(f"name='{settings.MODEL_NAME}'")
    for version in versions:
        if version.run_id == run_id:
            return version.version
    raise RuntimeError(f"Could not locate registered candidate model for run_id {run_id}")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run model quality gate before production promotion.")
    parser.add_argument("--run-id", required=True)
    parser.add_argument("--artifact-path", default=settings.ARTIFACT_PATH)
    parser.add_argument("--reference-path", default=os.getenv("REFERENCE_DATA_PATH", None))
    args = parser.parse_args()
    run_quality_gate(args.run_id, args.artifact_path, args.reference_path)
