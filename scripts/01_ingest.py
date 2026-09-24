"""
FISA-OPA Enterprise Risk Engine (ERM-X)
Step 1: Provision the SQLite database and load seed telemetry.
"""

import sqlite3
import os

# Ensure the database is created in the data/ folder regardless of where the script is run
DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fisa_risk_engine.db")

def provision_database():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # --- Table 1: Business Services (What the agency MUST deliver) ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS business_services (
        service_id TEXT PRIMARY KEY,
        name TEXT,
        tier INTEGER,
        max_tolerable_downtime_hrs REAL,
        business_owner TEXT
    );
    """)

    # --- Table 2: Risk Portfolio (Normalized telemetry from disparate sources) ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS risk_portfolio (
        risk_id TEXT PRIMARY KEY,
        source TEXT,
        system_component TEXT,
        service_id TEXT,
        description TEXT,
        inherent_risk_score INTEGER,
        control_id TEXT,
        control_effectiveness REAL,
        residual_risk_score REAL,
        status TEXT,
        FOREIGN KEY(service_id) REFERENCES business_services(service_id)
    );
    """)

    # --- Table 3: Agentic AI & Automation Controls (The emerging risk frontier) ---
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS ai_controls (
        control_id TEXT PRIMARY KEY,
        ai_risk_category TEXT,
        mitigation_type TEXT,
        description TEXT,
        is_enforced BOOLEAN
    );
    """)

    # --- Seed Data ---
    services_data = [
        ("SVC-01", "Citywide Bi-Weekly Payroll Engine", 1, 4.0, "Office of Payroll"),
        ("SVC-02", "Vendor Automated Clearing House (ACH) Dispatch", 1, 8.0, "Financial Systems"),
        ("SVC-03", "Employee Benefits & Open Enrollment Portal", 2, 24.0, "HR Operations")
    ]

    risks_data = [
        ("RSK-101", "Cloud/Infra", "AWS Transit Gateway", "SVC-01", "Hybrid cloud latency spike causing batch job timeouts", 8, "CTL-NET-01", 0.7, 2.4, "Open"),
        ("RSK-102", "Third-Party", "Cloud Hosting Vendor (Core FinTech)", "SVC-02", "Vendor SOC 2 Type II audit report overdue; no active SLA penalty tracking", 7, "CTL-TPRM-04", 0.4, 4.2, "Open"),
        ("RSK-103", "Agentic AI", "Autonomous Overtime Adjustment Agent", "SVC-01", "LLM agent has write-access to direct deposit ledger without manual check", 10, "CTL-AI-01", 0.2, 8.0, "Open"),
        ("RSK-104", "Vulnerability", "Legacy Oracle 11g Database", "SVC-03", "Unpatched CVE-2023-XXXX on premises database holding PII", 9, "CTL-SEC-09", 0.5, 4.5, "Remediating")
    ]

    ai_controls_data = [
        ("CTL-AI-01", "Excessive Agency", "Human-in-the-Loop (HITL)", "Mandatory dual-key approval for ledger delta > $5,000", 0),
        ("CTL-AI-02", "Prompt Injection", "Guardrail LLM", "Input sanitizer filtering system prompt extraction attempts", 1),
        ("CTL-AI-03", "Data Leakage", "Deterministic Tokenizer", "Redaction of NYS Tax IDs prior to LLM model context ingestion", 1)
    ]

    cursor.executemany("INSERT OR REPLACE INTO business_services VALUES (?, ?, ?, ?, ?)", services_data)
    cursor.executemany("INSERT OR REPLACE INTO risk_portfolio VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", risks_data)
    cursor.executemany("INSERT OR REPLACE INTO ai_controls VALUES (?, ?, ?, ?, ?)", ai_controls_data)

    conn.commit()
    conn.close()
    print(f"✅ FISA-OPA Risk Database provisioned at: {DB_PATH}")


if __name__ == "__main__":
    provision_database()