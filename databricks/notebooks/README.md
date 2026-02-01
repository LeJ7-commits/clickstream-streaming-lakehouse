## Streaming Operations & Reliability

### Stream Monitoring
Stream health is monitored by querying the Bronze Delta table for:
- latest ingest timestamp
- total processed events

Checkpoint directories are stored in S3 and track offsets and commit logs.

### Failure Recovery
The pipeline uses Structured Streaming checkpoints.
If the job stops or fails:
- restart resumes from the last committed offset
- already processed files are not reprocessed
- exactly-once semantics are preserved

### Data Quality & Quarantine
Malformed or incomplete events are not dropped.
They are routed to a quarantine Delta table for inspection and replay.
