# Architecture Overview

This repository implements a modular MLOps lifecycle platform with the following core components:

- **Training & Model Registry:** Automated training pipelines log candidate models to MLflow and register them for production comparison.
- **Automated Governance:** A challenger pattern quality gate benchmarks a candidate model against the current production model and applies bias and drift checks before promotion.
- **Data & Model Observability:** Adds Evidently-based drift reporting and structured metrics for Prometheus, plus JSON logs for Datadog/ELK ingestion.
- **Infrastructure as Code:** Terraform modules for GCP Cloud Run, AWS App Runner, and artifact registry provisioning.
- **Production Serving:** FastAPI wrapper with `/health`, `/ready`, and `/metrics` to meet Kubernetes and observability requirements.

## Architectural Patterns

- **Challenger Pattern:** The governance module compares a new candidate to the golden production model and only promotes when it improves performance and passes compliance checks.
- **Blue/Green Deployment:** CI/CD workflow deploys a green environment before traffic switch, enabling zero-downtime rollouts.
- **Defense-in-Depth:** Drift, bias, and schema validation are all enforced before deployment, reducing legal and operational risk.
