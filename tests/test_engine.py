import sys
import os

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from scripts.engine import calculate_executive_metrics


def test_dataframe_not_empty():
    df = calculate_executive_metrics()
    assert len(df) == 4, "Expected 4 risks in the portfolio."


def test_ai_risk_is_highest():
    df = calculate_executive_metrics()
    top_risk = df.iloc[0]
    assert top_risk["risk_id"] == "RSK-103", "AI agent should be the top-weighted risk."
    assert top_risk["weighted_risk_score"] == 12.00, "RSK-103 score should be 12.00."


def test_tier_multiplier_applied():
    df = calculate_executive_metrics()
    rsk_101 = df[df["risk_id"] == "RSK-101"].iloc[0]
    # 8 * (1 - 0.7) * 1.5 = 3.6 ... wait, but seed says residual is 2.4?
    # Our formula recalculates: 8 * 0.3 * 1.5 = 3.6
    # NOTE: The seed's residual_risk_score column is stale; our engine recalculates dynamically.
    assert rsk_101["weighted_risk_score"] == 3.6, "Tier 1 multiplier should produce 3.6."


if __name__ == "__main__":
    test_dataframe_not_empty()
    test_ai_risk_is_highest()
    test_tier_multiplier_applied()
    print("✅ All tests passed.")