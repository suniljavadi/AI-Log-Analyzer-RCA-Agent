from app.services.analyzer import LogAnalyzer
from app.services.catalog import build_incidents


def test_sql_timeout_is_high_and_grounded():
    result = LogAnalyzer(build_incidents()).analyze("""Job: Customer_Load
Package: Customer_Master
Timestamp: 2026-09-15 10:30:00
ERROR:
SQL timeout expired.
Execution time: 42 minutes
Expected execution time: 8 minutes
""")
    assert result.error_type == "SQL Timeout"
    assert result.severity == "HIGH"
    assert result.likely_root_cause
    assert result.confidence >= 80
    assert result.approval_required is True
    assert result.actions[0]["status"] == "approval_required"


def test_malformed_unknown_log_recovers():
    result = LogAnalyzer([]).analyze("A strange application event occurred with no known signature.")
    assert result.error_type == "Unknown Error"
    assert result.severity == "MEDIUM"
    assert result.hypotheses


def test_approved_actions_are_simulated_only():
    result = LogAnalyzer(build_incidents()).analyze("ERROR:\nfile not found in landing zone", approve_actions=True)
    assert result.approval_required is False
    assert all(action["status"] == "simulated" for action in result.actions)
