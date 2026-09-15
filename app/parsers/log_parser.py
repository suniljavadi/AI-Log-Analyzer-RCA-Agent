import re
from datetime import datetime
from typing import Any


class LogParseError(ValueError):
    pass


class LogParser:
    patterns = {
        "job": r"(?im)^Job:\s*(.+)$",
        "package": r"(?im)^Package:\s*(.+)$",
        "timestamp": r"(?im)^Timestamp:\s*(.+)$",
        "error_message": r"(?ims)^ERROR:\s*(.+?)(?=\n\s*\n|\nExecution time:|\Z)",
        "duration": r"(?im)^Execution time:\s*([\d.]+)\s*(minutes?|seconds?|hours?)",
        "expected_duration": r"(?im)^Expected execution time:\s*([\d.]+)\s*(minutes?|seconds?|hours?)",
        "system": r"(?im)^System:\s*(.+)$",
    }

    def parse(self, raw_log: str) -> dict[str, Any]:
        if not raw_log or len(raw_log.strip()) < 10:
            raise LogParseError("Log is empty or too short")
        result: dict[str, Any] = {"raw_log": raw_log, "metadata": {}}
        for key, pattern in self.patterns.items():
            match = re.search(pattern, raw_log)
            if match:
                value = match.group(1).strip()
                if key in {"duration", "expected_duration"}:
                    value = self._to_minutes(float(match.group(1)), match.group(2))
                result[key] = value
        if "error_message" not in result:
            result["error_message"] = raw_log.strip().splitlines()[-1]
        if "timestamp" in result:
            try:
                result["timestamp"] = datetime.fromisoformat(result["timestamp"])
            except ValueError:
                result["timestamp"] = datetime.now()
        else:
            result["timestamp"] = datetime.now()
        result.setdefault("job", "Unknown_Job")
        result.setdefault("system", "Application")
        result.setdefault("package", "Unknown_Package")
        result.setdefault("duration", None)
        result.setdefault("expected_duration", None)
        result["metadata"] = {"package": result["package"], "source": "synthetic_or_user_input"}
        return result

    @staticmethod
    def _to_minutes(value: float, unit: str) -> float:
        unit = unit.lower()
        return value / 60 if unit.startswith("second") else value * 60 if unit.startswith("hour") else value
