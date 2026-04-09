terraform {
  required_providers {
    google = {
      source  = "hashicorp/google"
      version = "~> 4.0"
    }
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "google" {
  project = var.gcp_project
  region  = var.gcp_region
}

provider "aws" {
  region = var.aws_region
}

module "artifact_registry" {
  source         = "./modules/artifact_registry"
  cloud_provider = var.cloud_provider
  region         = var.cloud_region
  repository_id  = var.repository_id
}

module "gcp_cloud_run" {
  source       = "./modules/gcp_cloud_run"
  providers    = { google = google }
  count        = var.cloud_provider == "gcp" ? 1 : 0
  project      = var.gcp_project
  region       = var.gcp_region
  service_name = var.service_name
  image        = var.container_image
}

module "aws_app_runner" {
  source       = "./modules/aws_app_runner"
  providers    = { aws = aws }
  count        = var.cloud_provider == "aws" ? 1 : 0
  service_name = var.service_name
  image        = var.container_image
}
