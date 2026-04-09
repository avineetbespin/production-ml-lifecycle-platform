output "artifact_repository_url" {
  value = module.artifact_registry.repository_url
}

output "service_endpoint" {
  value = var.cloud_provider == "gcp" ? module.gcp_cloud_run[0].service_url : module.aws_app_runner[0].service_url
  description = "The public endpoint for the deployed service"
}
