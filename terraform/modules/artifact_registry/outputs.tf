output "repository_url" {
  value = var.cloud_provider == "gcp" ? google_artifact_registry_repository.gcp_repo[0].repository_id : aws_ecr_repository.aws_repo[0].repository_url
}
