from datetime import datetime, timedelta

TEMPLATES = [
    ("SQL Timeout", "SQL timeout expired while loading customer records.", "Database query timeout.", "Review blocking and execution plan.", "HIGH"),
    ("SQL Deadlock", "Transaction was deadlocked on Customer table.", "Concurrent transactions contended for locks.", "Inspect deadlock graph and transaction order.", "HIGH"),
    ("Connection Failure", "Connection refused by database endpoint.", "Dependency unavailable or unreachable.", "Verify endpoint, network, and pool.", "HIGH"),
    ("Authentication Failure", "Login failed for service account.", "Credential or permission mismatch.", "Validate secret rotation and grants.", "MEDIUM"),
    ("API Timeout", "Upstream API timeout after 30 seconds.", "Upstream dependency latency.", "Inspect upstream latency and gateway limits.", "HIGH"),
    ("API 500", "HTTP 500 Internal Server Error from customer API.", "Unhandled upstream application exception.", "Inspect upstream trace and deployment.", "HIGH"),
    ("File Missing", "Required file not found in landing zone.", "Upstream delivery or path failure.", "Verify delivery and scheduler dependency.", "MEDIUM"),
    ("File Corruption", "Checksum mismatch detected in source file.", "Incomplete or corrupted transfer.", "Re-deliver file and verify checksum.", "HIGH"),
    ("SSIS Failure", "SSIS Data Flow Task failed validation.", "Package metadata or source schema drift.", "Review package and source schema.", "HIGH"),
    ("Network Failure", "Network unreachable while calling dependency.", "Network path or DNS failure.", "Check DNS, routing, and firewall telemetry.", "HIGH"),
    ("Memory Error", "Out of memory while processing batch.", "Batch exceeded process memory budget.", "Reduce batch size and inspect memory limits.", "HIGH"),
    ("Disk Space", "Disk full prevented log write.", "Insufficient filesystem capacity.", "Free capacity and review retention.", "CRITICAL"),
    ("Data Quality Failure", "Null constraint violation in CustomerId.", "Invalid source data.", "Quarantine records and contact data owner.", "HIGH"),
]


def build_incidents(count: int = 130) -> list[dict]:
    incidents = []
    base = datetime(2026, 1, 1, 8, 0, 0)
    for index in range(count):
        error_type, message, cause, resolution, severity = TEMPLATES[index % len(TEMPLATES)]
        incidents.append({"incident_id": f"INC-{index + 1:04d}", "timestamp": base + timedelta(hours=index * 7), "system": ["SQL Server", "SSIS", "Customer API", "Data Lake"][index % 4], "job": ["Customer_Load", "Order_Load", "Product_Master", "Finance_Recon"][index % 4], "error_type": error_type, "error_message": message, "root_cause": cause, "resolution": resolution, "severity": severity, "duration": float(5 + (index % 45)), "metadata": {"synthetic": True, "batch": index % 10, "source": "portfolio_generator"}})
    return incidents
