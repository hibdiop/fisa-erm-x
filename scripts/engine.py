"""
FISA-OPA Enterprise Risk Engine (ERM-X)
Step 2: Analytical pipeline. Calculates weighted residual risk.
"""

import sqlite3
import pandas as pd
import os

DB_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "fisa_risk_engine.db")


def calculate_executive_metrics() -> pd.DataFrame:
    """
    Returns a prioritized DataFrame of enterprise risks.
    Weighted Risk = Inherent * (1 - Control Effectiveness) * Tier Multiplier
    Tier 1 (Mission Critical) risks are multiplied by 1.5x.
    """
    conn = sqlite3.connect(DB_PATH)

    query = """
    SELECT 
        r.risk_id,
        r.source,
        b.name AS service_impacted,
        b.tier,
        b.max_tolerable_downtime_hrs,
        r.description,
        r.inherent_risk_score,
        r.control_effectiveness,
        ROUND(
            r.inherent_risk_score * (1.0 - r.control_effectiveness) 
            * (CASE WHEN b.tier = 1 THEN 1.5 ELSE 1.0 END), 
            2
        ) AS weighted_risk_score,
        r.status,
        c.ai_risk_category,
        c.is_enforced AS control_enforced
    FROM risk_portfolio r
    JOIN business_services b ON r.service_id = b.service_id
    LEFT JOIN ai_controls c ON r.control_id = c.control_id
    ORDER BY weighted_risk_score DESC;
    """

    df = pd.read_sql_query(query, conn)
    conn.close()
    return df


if __name__ == "__main__":
    df = calculate_executive_metrics()
    print("\n=== FISA-OPA EXECUTIVE RISK PRIORITIZATION QUEUE ===\n")
    print(df[["risk_id", "service_impacted", "weighted_risk_score", "source", "status"]].to_string(index=False))