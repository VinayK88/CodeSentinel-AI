import json
from pathlib import Path
import streamlit as st

st.set_page_config(page_title="CodeSentinel AI", page_icon="🛡️", layout="wide", initial_sidebar_state="expanded")
report = json.loads(Path("reports/baseline.json").read_text())
findings = report["findings"]

st.markdown("""
<style>
html,body,[class*="css"]{font-family:-apple-system,BlinkMacSystemFont,"SF Pro Display","SF Pro Text","Helvetica Neue",Arial,sans-serif;color:#1d1d1f}
:root{--blue:#0071e3;--ink:#1d1d1f;--muted:#6e6e73;--bg:#f5f5f7;--card:#fff;}
[data-testid="stAppViewContainer"]{background:var(--bg);} [data-testid="stHeader"]{background:transparent;}
[data-testid="stSidebar"]{background:#fff;border-right:1px solid #e5e5ea;} .block-container{padding:2rem 2.4rem 4rem;max-width:1500px;}
h1,h2,h3{letter-spacing:-.035em;color:var(--ink);} .hero{background:linear-gradient(135deg,#fff 0%,#f8fbff 100%);border:1px solid #e5e5ea;border-radius:32px;padding:38px 42px;margin-bottom:22px;box-shadow:0 14px 36px rgba(0,0,0,.045)}
.eyebrow{color:var(--blue);font-weight:700;font-size:.78rem;letter-spacing:.11em;text-transform:uppercase}.hero h1{font-size:3.3rem;letter-spacing:-.052em;margin:.15rem 0 .35rem}.hero p{font-size:1.12rem;line-height:1.55;color:var(--muted);max-width:900px}.pill{display:inline-block;background:#eef6ff;color:#0066cc;border:1px solid #d8eaff;border-radius:999px;padding:7px 12px;margin:10px 6px 0 0;font-size:.78rem;font-weight:650}
[data-testid="stMetric"]{background:#fff;border:1px solid #e5e5ea;border-radius:24px;padding:18px 20px;box-shadow:0 8px 26px rgba(0,0,0,.035);min-height:116px}[data-testid="stMetricLabel"]{color:var(--muted);font-weight:600}[data-testid="stMetricValue"]{color:var(--ink);font-size:1.9rem;font-weight:700;letter-spacing:-.035em}
.section{font-size:1.45rem;font-weight:700;color:var(--ink);margin:28px 0 12px}.note{background:#fff;border:1px solid #e5e5ea;border-radius:18px;padding:15px 18px;color:var(--muted)}
div[data-testid="stDataFrame"]{border:1px solid #e5e5ea;border-radius:18px;overflow:hidden;background:#fff;} .stTabs [data-baseweb="tab-list"]{gap:8px}.stTabs [data-baseweb="tab"]{background:white;border-radius:999px;padding:8px 16px;border:1px solid #e5e5ea}
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## CodeSentinel **AI**")
    st.caption("Application Security Intelligence")
    st.markdown("---")
    st.markdown("**Overview**")
    st.markdown("Findings")
    st.markdown("PR Reviews")
    st.markdown("Validation")
    st.markdown("Remediation")
    st.markdown("Reports")
    st.markdown("---")
    st.caption("Synthetic / offline portfolio demo")

st.markdown("""<div class="hero"><div class="eyebrow">AI-Native AppSec</div><h1>CodeSentinel <span style="color:#0071e3">AI</span></h1><p>Secure code review that connects findings to validation, developer disposition, remediation, and verified closure.</p><span class="pill">PR security review</span><span class="pill">CWE mapping</span><span class="pill">Finding validation</span><span class="pill">Remediation intelligence</span></div>""", unsafe_allow_html=True)

eval_ = report["evaluation"]
critical = sum(1 for x in findings if x["severity"] == "critical")
high = sum(1 for x in findings if x["severity"] == "high")
medium = sum(1 for x in findings if x["severity"] == "medium")
low = sum(1 for x in findings if x["severity"] == "low")
cwe_count = len({x["cwe"] for x in findings})
avg_confidence = sum(float(x["confidence"]) for x in findings) / max(len(findings),1)
avg_risk = sum(float(x["risk_score"]) for x in findings) / max(len(findings),1)
max_risk = max((float(x["risk_score"]) for x in findings), default=0.0)
unique_lines = len({x["line"] for x in findings})
severity_levels = len({x["severity"] for x in findings})

kpi_rows=[
    [("Findings",report["finding_count"]),("Critical / high",report["high_risk_count"]),("Precision",f"{eval_['precision']:.0%}"),("Recall",f"{eval_['recall']:.0%}"),("CWE coverage",cwe_count)],
    [("Critical",critical),("High",high),("Medium",medium),("Low",low),("Severity levels",severity_levels)],
    [("Avg confidence",f"{avg_confidence:.0%}"),("Avg risk",f"{avg_risk:.3f}"),("Max risk",f"{max_risk:.3f}"),("Unique lines",unique_lines),("Review mode","Human-gated")],
]
for row in kpi_rows:
    cols=st.columns(5)
    for col,(label,value) in zip(cols,row): col.metric(label,value)

st.markdown('<div class="section">Security posture</div>', unsafe_allow_html=True)
a,b,c = st.columns([1.4,1,1])
with a:
    st.markdown("**Risk trend · illustrative dashboard view**")
    st.line_chart({"High risk":[5,7,6,8,7,9],"Validated":[3,4,5,6,6,7]}, height=250)
with b:
    st.markdown("**Severity mix**")
    st.bar_chart({"Critical":critical,"High":high,"Medium":medium,"Low":low}, height=250)
with c:
    st.markdown("**Top CWE families**")
    for f in sorted(findings, key=lambda x:x["risk_score"], reverse=True)[:5]:
        st.progress(float(f["risk_score"]), text=f"{f['cwe']} · {f['title']}")

st.markdown('<div class="section">Review workspace</div>', unsafe_allow_html=True)
t1,t2,t3 = st.tabs(["Validated findings","Remediation funnel","Evidence"])
with t1:
    rows=[{"Severity":x["severity"].upper(),"CWE":x["cwe"],"Finding":x["title"],"Confidence":x["confidence"],"Risk":x["risk_score"],"Line":x["line"]} for x in findings]
    st.dataframe(rows,use_container_width=True,hide_index=True)
with t2:
    stages={"Detected":report["finding_count"],"Validated":report["finding_count"],"Prioritized":report["high_risk_count"],"Review-ready":report["high_risk_count"]}
    st.bar_chart(stages, horizontal=True, height=260)
    st.caption("The public replay demonstrates the lifecycle mechanics; production acceptance and closure require developer/analyst feedback telemetry.")
with t3:
    for f in findings:
        with st.expander(f"{f['severity'].upper()} · {f['cwe']} · {f['title']}"):
            st.code(f["evidence"], language="python")
            st.write(f"Confidence **{f['confidence']:.0%}** · Risk score **{f['risk_score']:.3f}** · Line **{f['line']}**")

st.markdown("""<div class="note"><b>Evaluation boundary.</b> This dashboard uses deterministic synthetic PR diffs. Metrics demonstrate implementation and evaluation mechanics, not production security efficacy.</div>""", unsafe_allow_html=True)
