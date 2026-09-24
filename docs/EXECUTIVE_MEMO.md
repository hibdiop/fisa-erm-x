# FISA-OPA Enterprise Risk Engine (ERM-X)
## Executive Briefing: Unified Risk Telemetry & Agentic AI Governance

**Prepared by:** [Your Name]
**Date:** [Today's Date]
**Audience:** FISA-OPA Director, CISO, Office of Payroll

---

### 1. Problem Statement
Traditional static spreadsheets obscure the correlation between infrastructure uptime, vendor posture, and payroll finality. FISA-OPA currently lacks a single, quantified view of how technical vulnerabilities translate into operational disruption of mission-critical services like bi-weekly payroll and ACH dispatch.

### 2. Technical Design
I have built a working prototype (ERM-X) that normalizes risk telemetry from four disparate sources:
- **Cloud/Infrastructure** vulnerabilities
- **Third-Party/Vendor** audit lapses
- **Legacy** on-premises CVEs
- **Agentic AI** workflow permissions

These are correlated against a registry of Tier 1–3 NYC business services, with each risk dynamically weighted by:

$$
Weighted Risk = Inherent Risk × (1 − Control Effectiveness) × Tier Multiplier
$$

---


Tier 1 (Mission Critical) services receive a 1.5× multiplier.

### 3. Key Finding
**The single largest enterprise risk is RSK-103**: an autonomous LLM agent with direct write-access to the direct deposit ledger, scoring **12.00 / 15.0**. This is higher than any legacy vulnerability or vendor lapse. The agent's controls (Human-in-the-Loop for ledger deltas > $5,000) are currently **not enforced**.

### 4. Agentic AI Governance Framework: The Triple-Gate Rule
For any autonomous LLM operating in payroll reconciliation, I recommend the following mandatory controls:

| Gate | Control | Purpose |
|------|---------|---------|
| **Gate 1** | System-Prompt Injection Sanitization | Prevents adversarial inputs from overriding agent instructions. |
| **Gate 2** | Deterministic Tokenization of Employee Tax IDs | Ensures PII never enters the LLM context window. |
| **Gate 3** | Mandatory Human-in-the-Loop (HITL) Approval | Requires dual-key approval for any financial state change > $5,000. |

### 5. Scalability Plan
This prototype runs locally on SQLite, pandas, and Streamlit. In production, the ingestion layer can be swapped for:
- **Snowflake / Databricks** for the analytical warehouse
- **ServiceNow GRC** or **Archer** as the system of record
- **Power BI** for executive distribution
- **Nightly API ingest scripts** to replace manual data pulls

The SQL schema and Python engine are portable and require no rewrite.

---

### Appendix: Screenshot
[Insert your Streamlit dashboard screenshot here]

