# audit.py
# Writes one audit line per tool attempt, without names, scores, or other sensitive values.

import json
from datetime import datetime, timezone

AUDIT_FILE = "audit_log.jsonl"


def record_tool_attempt(tool_name, source, outcome):
    entry = {
        "time": datetime.now(timezone.utc).isoformat(),
        "event": "tool_attempt",
        "tool": tool_name,
        "source": source,
        "outcome": outcome,
    }
    with open(AUDIT_FILE, "a", encoding="utf-8") as file:
        file.write(json.dumps(entry) + "\n")