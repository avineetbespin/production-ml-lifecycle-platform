# Deployment Guide

This project includes a sample GitHub Actions pipeline for zero-downtime deployment.

## Workflow Steps

1. **Quality Gate**: Train candidate model, benchmark against production, run bias/fairness checks, and validate drift.
2. **Green Deployment**: Deploy new version to a green environment without affecting existing production traffic.
3. **Smoke Test**: Verify the green environment via health endpoint.
4. **Traffic Switch**: Promote green to production after successful validation.

## Cloud Support

- **GCP**: Uses `terraform/modules/gcp_cloud_run` for Cloud Run service deployment.
- **AWS**: Uses `terraform/modules/aws_app_runner` for App Runner deployments.
- **Artifact Registry**: Creates container artifact storage in either GCP Artifact Registry or AWS ECR.
