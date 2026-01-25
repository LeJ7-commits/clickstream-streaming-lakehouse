variable "project_name" {
  type        = string
  description = "Short project name used for naming AWS resources."
  default     = "realtime-lakehouse"
}

variable "environment" {
  type        = string
  description = "Environment tag."
  default     = "demo"
}

variable "aws_region" {
  type        = string
  description = "AWS region to deploy into."
  default     = "eu-north-1"
}

variable "s3_bucket_name" {
  type        = string
  description = "Manually created S3 bucket name for the lakehouse."
}