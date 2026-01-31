# Silver streaming transformation
# Bronze → Silver (clean + dedupe + watermark)

from pyspark.sql.functions import *
from pyspark.sql.types import *

# ---------- PATHS ----------
S3_BUCKET = "lej7-s3-databricks-realtime-04140428"

BRONZE_PATH = f"s3://{S3_BUCKET}/delta/bronze_clickstream/"
SILVER_PATH = f"s3://{S3_BUCKET}/delta/silver_clickstream/"
CHECKPOINT_PATH = f"s3://{S3_BUCKET}/checkpoints/silver_clickstream/"
QUARANTINE_PATH = f"s3://{S3_BUCKET}/delta/quarantine_clickstream/"

# ---------- STREAM READ ----------
bronze_stream = spark.readStream.format("delta").load(BRONZE_PATH)

# ---------- DATA QUALITY ----------
valid = bronze_stream.filter(
    col("user_id").isNotNull() &
    col("event_id").isNotNull() &
    col("event_time").isNotNull()
)

invalid = bronze_stream.subtract(valid)

# ---------- WATERMARK + DEDUPE ----------
silver = (
    valid
    .withWatermark("event_time", "10 minutes")
    .dropDuplicates(["event_id"])
)

# ---------- WRITE SILVER ----------
silver_query = (
    silver.writeStream
        .format("delta")
        .option("checkpointLocation", CHECKPOINT_PATH)
        .trigger(availableNow=True)
        .outputMode("append")
        .start(SILVER_PATH)
)

# ---------- WRITE QUARANTINE ----------
quarantine_query = (
    invalid.writeStream
        .format("delta")
        .option("checkpointLocation", CHECKPOINT_PATH + "_bad/")
        .trigger(availableNow=True)
        .outputMode("append")
        .start(QUARANTINE_PATH)
)

silver_query.awaitTermination()
quarantine_query.awaitTermination()