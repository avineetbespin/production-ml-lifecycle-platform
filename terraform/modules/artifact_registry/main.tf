resource "google_artifact_registry_repository" "gcp_repo" {
  count       = var.cloud_provider == "gcp" ? 1 : 0
  provider    = google
  project     = var.project
  location    = var.region
  repository_id = var.repository_id
  format      = "DOCKER"
  description = "Container Artifact Registry for model serving"
}

resource "aws_ecr_repository" "aws_repo" {
  count = var.cloud_provider == "aws" ? 1 : 0
  name  = var.repository_id
}
