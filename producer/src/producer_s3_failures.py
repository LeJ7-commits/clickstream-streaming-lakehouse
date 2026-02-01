def generate_event():
    # 5% malformed events
    if random.random() < 0.05:
        return {
            "event_id": None,              # invalid
            "user_id": None,
            "event_type": "BROKEN_EVENT"
        }

    now = datetime.datetime.utcnow().isoformat()
    return {
        "event_id": str(uuid.uuid4()),
        "user_id": f"user_{random.randint(1, 100)}",
        "event_type": random.choice(EVENT_TYPES),
        "country": random.choice(COUNTRIES),
        "event_time": now,
        "page": f"/product/{random.randint(1, 50)}",
    }