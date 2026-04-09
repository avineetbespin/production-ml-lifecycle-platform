# Usage Guide

## Initialize Infrastructure

```bash
cd terraform
terraform init
terraform apply
```

## Train and Register

```bash
python src/training/train.py --model-name production-model --artifact-path model
```

## Trigger the Deployment Pipeline

Push changes to `main` and the GitHub Actions workflow will run the quality gate and blue/green deployment.

## Observability and Monitoring

- `/health` and `/ready` for Kubernetes probes
- `/metrics` for Prometheus-compatible export
- Logs are emitted as structured JSON for Datadog or ELK ingestion
