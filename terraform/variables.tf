variable "cloud_provider" {
  type        = string
  description = "Choose between gcp and aws deployment targets"
  default     = "gcp"
}

variable "gcp_project" {
  type        = string
  description = "GCP project ID"
  default     = ""
}

variable "gcp_region" {
  type        = string
  description = "GCP region for Cloud Run"
  default     = "us-central1"
}

variable "aws_region" {
  type        = string
  description = "AWS region for App Runner"
  default     = "us-east-1"
}

variable "cloud_region" {
  type        = string
  description = "Generic region for artifact registry creation"
  default     = "us-central1"
}

variable "repository_id" {
  type        = string
  description = "Artifact repository name"
  default     = "mlops-artifacts"
}

variable "service_name" {
  type        = string
  description = "Service name for deployment"
  default     = "mlops-model-service"
}

variable "container_image" {
  type        = string
  description = "OCI image reference for the application"
  default     = "gcr.io/project-id/mlops-service:latest"
}
