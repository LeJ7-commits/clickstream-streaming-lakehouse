import os
import json
import uuid
import time
import random
import datetime
import tempfile
import boto3

# ---- Config from environment ----
AWS_REGION = os.getenv("AWS_REGION", "eu-north-1")
S3_BUCKET = os.getenv("S3_BUCKET", "YOUR_BUCKET_HERE")
S3_PREFIX = os.getenv("S3_PREFIX", "landing/clickstream")
BATCH_SECONDS = int(os.getenv("BATCH_SECONDS", "5"))
ROWS_PER_BATCH = int(os.getenv("ROWS_PER_BATCH", "50"))

s3 = boto3.client("s3", region_name=AWS_REGION)

EVENT_TYPES = ["page_view", "add_to_cart", "purchase"]
COUNTRIES = ["SE", "DE", "US", "FR", "NL"]

def generate_event():
    now = datetime.datetime.utcnow().isoformat()

    return {
        "event_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1, 100)}",
        "event_type": random.choice(EVENT_TYPES),
        "country": random.choice(COUNTRIES),
        "event_time": now,
        "page": f"/product/{random.randint(1, 50)}",
    }

def upload_batch(events):
    now = datetime.datetime.utcnow()
    ingest_date = now.strftime("%Y-%m-%d")
    hour = now.strftime("%H")

    key_prefix = f"{S3_PREFIX}/ingest_date={ingest_date}/hour={hour}"
    object_name = f"{key_prefix}/batch_{uuid.uuid4()}.jsonl"

    with tempfile.NamedTemporaryFile(mode="w", delete=False) as f:
        for e in events:
            f.write(json.dumps(e) + "\n")
        temp_path = f.name

    s3.upload_file(temp_path, S3_BUCKET, object_name)

    print(f"Uploaded {len(events)} events → s3://{S3_BUCKET}/{object_name}")

def main():
    print("Starting S3 micro-batch producer...")
    print(f"Bucket: {S3_BUCKET}")
    print(f"Prefix: {S3_PREFIX}")
    print(f"Batch every {BATCH_SECONDS}s, rows={ROWS_PER_BATCH}")

    while True:
        events = [generate_event() for _ in range(ROWS_PER_BATCH)]
        upload_batch(events)
        time.sleep(BATCH_SECONDS)

if __name__ == "__main__":
    main()
