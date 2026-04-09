# production-ml-lifecycle-platform

A modular, production-ready MLOps framework that automates the transition from model training to zero-downtime deployment.

## Core Capabilities

- Automated Governance using the Challenger Pattern and a Model Quality Gate
- Data Drift and Bias/Fairness checks before promotion
- FastAPI production serving with `/health`, `/ready`, and Prometheus `/metrics`
- Terraform modules for cloud infrastructure on GCP Cloud Run or AWS App Runner
- Blue/Green deployment strategy in GitHub Actions
- Integration-ready JSON logging and structured telemetry

## Implementation Guide

1. Initialize Infra:
   ```bash
   cd terraform
   terraform init
   terraform apply
   ```
2. Train & Register:
   ```bash
   python src/training/train.py --model-name production-model --artifact-path model
   ```
3. Run locally with Docker:
   ```bash
   docker build -t production-ml-lifecycle-platform:latest .
   docker run --rm -p 8000:8000 production-ml-lifecycle-platform:latest
   ```
4. Trigger Pipeline:
   - Push to `main` to trigger the automated quality gate and deployment.

## Architectural Trade-offs

- **Modularity over one-off scripts:** The design separates training, governance, observability, and serving into dedicated packages so teams can evolve each layer independently.
- **Challenger Pattern vs. simple promotion:** Comparing a candidate model to the current production model reduces regression risk, at the cost of needing a robust benchmark dataset and MLflow integration.
- **Blue/Green deployment:** This approach trades extra infrastructure for near-zero downtime and safe rollback capability.
- **Evidently for drift detection:** Using Evidently standardizes drift reporting and creates a clear gate, but it requires maintaining reference datasets and data contracts.
- **Terraform IaC:** Infrastructure as Code ensures repeatability and auditability, even though it requires writing provider-specific modules for both AWS and GCP.

## Strategic ROI

- Zero-Downtime: Blue/Green deployment supports 99.9% availability during updates.
- Risk Mitigation: Automated bias and drift detection reduce legal and operational risk.
- Developer Velocity: Standardized CI/CD templates let engineers focus on modeling instead of infrastructure.
