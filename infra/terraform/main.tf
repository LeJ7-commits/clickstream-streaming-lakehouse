terraform {
  required_version = ">= 1.5.0"
}

provider "aws" {
  region = var.aws_region
}

# No resources managed by Terraform in this phase.
# S3 bucket is created manually, and Databricks External Location is set up via Quickstart CloudFormation.