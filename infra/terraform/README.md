# Infrastructure (Terraform)

This folder provisions AWS resources for the project.

## What Terraform manages
- Amazon Kinesis Data Stream (clickstream ingress)

## What Terraform does NOT manage
Databricks-to-S3 access is configured using Databricks External Location Quickstart (CloudFormation) from the Databricks UI.  
This keeps the repo simple and avoids hard-coding Databricks account-specific identifiers.

## Deploy

From this directory:

```bash
terraform init
terraform fmt
terraform validate
terraform plan
terraform apply
