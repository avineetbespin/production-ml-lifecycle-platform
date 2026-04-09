variable "service_name" {
  type = string
}

variable "image" {
  type = string
}

variable "connection_arn" {
  type        = string
  description = "Optional AWS App Runner connection ARN for private registries"
  default     = ""
}
