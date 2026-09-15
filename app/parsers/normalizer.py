import re


class LogNormalizer:
    def normalize(self, parsed: dict) -> dict:
        normalized = dict(parsed)
        message = str(normalized.get("error_message", "")).lower()
        normalized["normalized_message"] = re.sub(r"\d+", "<number>", message)
        normalized["error_type"] = self.classify(message)
        return normalized

    @staticmethod
    def classify(message: str) -> str:
        rules = [
            ("SQL Timeout", ("sql timeout", "query timeout", "execution time")),
            ("SQL Deadlock", ("deadlock", "transaction was deadlocked")),
            ("Connection Failure", ("connection refused", "could not connect", "connection failure")),
            ("Authentication Failure", ("login failed", "authentication", "invalid password")),
            ("API Timeout", ("api timeout", "upstream timeout", "gateway timeout")),
            ("API 500", ("http 500", "internal server error", "status code 500")),
            ("File Missing", ("file not found", "missing file", "no such file")),
            ("File Corruption", ("corrupt", "checksum", "invalid format")),
            ("SSIS Failure", ("ssis", "package failed", "data flow task")),
            ("Network Failure", ("network unreachable", "dns", "socket")),
            ("Memory Error", ("out of memory", "memoryerror", "heap")),
            ("Disk Space", ("disk full", "no space", "disk space")),
            ("Data Quality Failure", ("data quality", "null constraint", "duplicate key", "schema mismatch")),
        ]
        for error_type, terms in rules:
            if any(term in message for term in terms):
                return error_type
        return "Unknown Error"
