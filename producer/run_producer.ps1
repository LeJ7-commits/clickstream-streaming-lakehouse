$env:AWS_REGION="eu-north-1"
$env:S3_BUCKET="lej7-s3-databricks-realtime-04140428"
$env:S3_PREFIX="landing/clickstream"
$env:BATCH_SECONDS="5"
$env:ROWS_PER_BATCH="50"

python src/producer_s3.py