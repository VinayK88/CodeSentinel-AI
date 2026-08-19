import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="CodeSentinel AI", layout="wide")
st.title("CodeSentinel AI — PR Security Review")
report = json.loads(Path("reports/baseline.json").read_text())
cols=st.columns(4)
cols[0].metric("Synthetic precision", report["evaluation"]["precision"])
cols[1].metric("Synthetic recall", report["evaluation"]["recall"])
cols[2].metric("Findings", report["finding_count"])
cols[3].metric("Critical / high", report["high_risk_count"])
st.subheader("Validated findings")
st.dataframe(report["findings"], use_container_width=True)
st.caption("Synthetic/offline demo — metrics demonstrate evaluation mechanics, not production efficacy.")
