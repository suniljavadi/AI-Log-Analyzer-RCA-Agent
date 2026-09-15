import json
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from app.services.catalog import build_incidents

output = Path("synthetic_logs")
output.mkdir(exist_ok=True)
incidents = build_incidents(260)
Path("data").mkdir(exist_ok=True)
with Path("data/historical_incidents.json").open("w", encoding="utf-8") as file:
    json.dump([{**item, "timestamp": item["timestamp"].isoformat()} for item in incidents], file, indent=2)
for index, incident in enumerate(incidents, 1):
    content = f"Job: {incident['job']}\nSystem: {incident['system']}\nTimestamp: {incident['timestamp'].isoformat()}\n\nERROR:\n{incident['error_message']}\n\nExecution time: {incident['duration']} minutes\nExpected execution time: 8 minutes\n"
    Path(output / f"incident_{index:04d}.log").write_text(content, encoding="utf-8")
print(f"Generated {len(incidents)} synthetic incidents")
