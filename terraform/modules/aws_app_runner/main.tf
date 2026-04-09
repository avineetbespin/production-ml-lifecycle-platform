resource "aws_app_runner_service" "app_runner" {
  service_name = var.service_name

  source_configuration {
    authentication_configuration {
      connection_arn = var.connection_arn
    }

    image_repository {
      image_identifier      = var.image
      image_repository_type = "ECR"
      image_configuration {
        port = "8000"
      }
    }
  }
}
