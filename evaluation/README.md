# Evaluation Guide

The public golden fixture is `golden-dataset-v1.jsonl` and contains synthetic operational-analysis cases.

## Metrics

Track classification accuracy, unknown handling, incident retrieval, evidence completeness, root-cause proxy accuracy, severity, confidence calibration, corrections, and approval safety.

## Observability

Record request ID, parser and corpus versions, evidence IDs, tool names, confidence, severity, duration, and action status. Redact secrets and personal data.

## Release Checks

Require safe malformed-log handling, evidence labeling, confidence limits, injection resistance, and approval-gated actions.
