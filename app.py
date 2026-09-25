"""
FISA-OPA Enterprise Risk Engine (ERM-X)
Step 3: Executive Dashboard (Streamlit)
"""

import streamlit as st
import pandas as pd
from scripts.engine import calculate_executive_metrics


st.set_page_config(page_title="Risk Telemetry", layout="wide")

st.title("Enterprise Risk & AI Governance Telemetry")
st.caption("Unified view: Cybersecurity, Vendor, Cloud, and Agentic AI risk mapped to mission-critical NYC services.")

df = calculate_executive_metrics()

# --- Top KPI Row ---
col1, col2, col3, col4 = st.columns(4)
col1.metric("Highest Weighted Risk", f"{df['weighted_risk_score'].max():.2f} / 15.0")
col2.metric("Critical Tier-1 Exposures", len(df[df['tier'] == 1]))
col3.metric("Open Risks", len(df[df['status'] == 'Open']))
col4.metric(
    "Unenforced AI Guardrails",
    len(df[(df['control_enforced'] == 0) & (df['source'] == 'Agentic AI')])
)

st.divider()

# --- Executive Prioritization Queue ---
st.markdown("### 🎯 Actionable Executive Prioritization Queue")
st.dataframe(
    df[["risk_id", "source", "service_impacted", "description", "weighted_risk_score", "status"]],
    use_container_width=True,
    hide_index=True
)

st.divider()

# --- AI Risk Spotlight ---
st.markdown("### 🤖 Agentic AI Risk Isolation Spotlight")
ai_slice = df[df["source"] == "Agentic AI"]

if ai_slice.empty:
    st.success("No unmitigated agentic AI risks detected.")
else:
    for _, row in ai_slice.iterrows():
        st.error(f"**Critical Exposure in {row['service_impacted']}** — Risk ID: {row['risk_id']}")
        st.write(f"- **Description:** {row['description']}")
        st.write(f"- **Control Gap:** {row['ai_risk_category']} safeguard is {'ENFORCED' if row['control_enforced'] else 'NOT ENFORCED'}")
        st.write(f"- **Operational Consequence:** Potential unauthorized disbursements bypassing City Comptroller audit gates.")
        st.write(f"- **Weighted Risk Score:** {row['weighted_risk_score']} / 15.0")

st.divider()

# --- Business Impact Context ---
st.markdown("### 🏛️ Business Service Impact Reference")
st.dataframe(
    df[["service_impacted", "tier", "max_tolerable_downtime_hrs", "weighted_risk_score"]]
      .drop_duplicates(subset=["service_impacted"])
      .sort_values("tier"),
    use_container_width=True,
    hide_index=True
)