import os

import requests
import streamlit as st

st.set_page_config(page_title="AI Log Analyzer", page_icon="🧭", layout="wide")
st.title("AI Log Analyzer")
st.caption("Synthetic incident investigation with retrieval-grounded, approval-gated diagnosis")

sample = """Job: Customer_Load
Package: Customer_Master
Timestamp: 2026-09-15 10:30:00
System: SQL Server

ERROR:
SQL timeout expired.

Execution time: 42 minutes
Expected execution time: 8 minutes
"""
raw_log = st.text_area("Log input", sample, height=220)
col1, col2 = st.columns([1, 3])
with col1:
    approve = st.checkbox("Simulate human approval", value=False)
    analyze = st.button("Analyze incident", type="primary", use_container_width=True)

if analyze:
    try:
        api_url = os.getenv("API_URL", "http://localhost:8000")
        response = requests.post(f"{api_url}/api/v1/analyze", json={"raw_log": raw_log, "approve_actions": approve}, timeout=20)
        response.raise_for_status()
        result = response.json()
        st.success(f"{result['severity']} severity | {result['error_type']} | confidence {result['confidence']}%")
        left, right = st.columns(2)
        with left:
            st.subheader("Diagnosis")
            st.write(result["likely_root_cause"])
            st.write("**Observed facts**")
            for fact in result["observed_facts"]:
                st.write(f"- {fact}")
            st.write("**Evidence**")
            for evidence in result["evidence"]:
                st.write(f"- {evidence}")
            st.write("**Recommendations**")
            for item in result["recommendations"]:
                st.write(f"- {item}")
        with right:
            st.subheader("Alternative hypotheses")
            st.json(result["hypotheses"])
            st.subheader("Similar incidents")
            st.dataframe(result["similar_incidents"], use_container_width=True, hide_index=True)
        st.subheader("Timeline")
        st.json(result["timeline"])
        st.subheader("Approval-gated actions")
        st.json(result["actions"])
        with st.expander("Parsed log"):
            st.json(result["parsed_log"])
    except requests.RequestException as exc:
        st.error(f"API unavailable: {exc}. Start FastAPI with: uvicorn main:app --reload")
