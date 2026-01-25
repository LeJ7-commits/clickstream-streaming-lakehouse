output "aws_region" {
  value = var.aws_region
}

output "s3_bucket_name" {
  value = var.s3_bucket_name
}

output "s3_paths" {
  value = {
    landing     = "s3://${var.s3_bucket_name}/landing/clickstream/"
    bronze      = "s3://${var.s3_bucket_name}/delta/bronze_clickstream/"
    silver      = "s3://${var.s3_bucket_name}/delta/silver_clickstream/"
    gold        = "s3://${var.s3_bucket_name}/delta/gold_clickstream_kpis/"
    checkpoints = "s3://${var.s3_bucket_name}/checkpoints/"
  }
}