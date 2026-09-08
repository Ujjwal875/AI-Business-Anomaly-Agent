from __future__ import annotations

from pathlib import Path
import pandas as pd

METRICS = [
    "revenue",
    "orders",
    "conversion_rate",
    "traffic",
    "cost",
    "refunds",
]


def load_data(file_path: str | Path, sheet_name: str = "business_data") -> pd.DataFrame:
    """Load and validate the business metrics workbook."""
    df = pd.read_excel(file_path, sheet_name=sheet_name)
    df["date"] = pd.to_datetime(df["date"])
    df = df.sort_values("date").drop_duplicates("date").reset_index(drop=True)

    missing_columns = {"date", *METRICS} - set(df.columns)
    if missing_columns:
        raise ValueError(f"Missing required columns: {sorted(missing_columns)}")

    if df[METRICS].isna().any().any():
        raise ValueError("Input contains missing metric values.")

    return df


def detect_anomalies(
    df: pd.DataFrame,
    window: int = 7,
    threshold: float = 20.0,
) -> pd.DataFrame:
    """Compare each metric with its previous rolling baseline and flag anomalies."""
    result = df.copy()

    for metric in METRICS:
        # shift(1) prevents the current observation from influencing its baseline
        baseline = result[metric].shift(1).rolling(window=window, min_periods=1).mean()
        result[f"{metric}_baseline"] = baseline
        result[f"{metric}_deviation_pct"] = (
            (result[metric] - baseline) / baseline
        ) * 100
        result[f"{metric}_anomaly"] = (
            result[f"{metric}_deviation_pct"].abs() >= threshold
        )

    abs_deviations = [f"{m}_deviation_pct" for m in METRICS]
    result["max_deviation_pct"] = result[abs_deviations].abs().max(axis=1)

    def severity(value: float) -> str:
        if pd.isna(value) or value < threshold:
            return "Normal"
        if value >= 50:
            return "Critical"
        if value >= 30:
            return "High"
        return "Medium"

    result["severity"] = result["max_deviation_pct"].apply(severity)

    def anomaly_details(row: pd.Series) -> str:
        details = []
        for metric in METRICS:
            if row[f"{metric}_anomaly"]:
                deviation = row[f"{metric}_deviation_pct"]
                direction = "increased" if deviation > 0 else "decreased"
                details.append(f"{metric} {direction} by {abs(deviation):.1f}%")
        return ", ".join(details)

    result["anomaly_details"] = result.apply(anomaly_details, axis=1)
    return result


def explain_impact(row: pd.Series) -> str:
    """Create a rule-based business-impact explanation for detected movements."""
    impacts = []

    if row["revenue_anomaly"]:
        impacts.append(
            "Potential revenue loss."
            if row["revenue_deviation_pct"] < 0
            else "Revenue increased significantly and may indicate strong sales performance."
        )

    if row["orders_anomaly"]:
        impacts.append(
            "Lower order volume may be affecting sales performance."
            if row["orders_deviation_pct"] < 0
            else "Higher order volume may indicate increased customer demand."
        )

    if row["conversion_rate_anomaly"]:
        impacts.append(
            "Lower conversion may indicate weaker traffic quality or checkout performance."
            if row["conversion_rate_deviation_pct"] < 0
            else "Higher conversion may indicate improved customer engagement or purchase intent."
        )

    if row["traffic_anomaly"]:
        impacts.append(
            "Reduced traffic may be limiting the number of potential customers."
            if row["traffic_deviation_pct"] < 0
            else "Higher traffic may indicate increased customer interest."
        )

    if row["cost_anomaly"]:
        impacts.append(
            "Higher costs may put pressure on profitability."
            if row["cost_deviation_pct"] > 0
            else "Lower costs may improve profitability."
        )

    if row["refunds_anomaly"]:
        impacts.append(
            "Higher refunds may indicate product, delivery, or customer-experience issues."
            if row["refunds_deviation_pct"] > 0
            else "Lower refunds may indicate improved customer satisfaction, though the unusual change should still be investigated."
        )

    return " ".join(impacts) or "No significant anomalies detected."


def prepare_results(file_path: str | Path) -> pd.DataFrame:
    df = load_data(file_path)
    result = detect_anomalies(df)
    result["business_impact"] = result.apply(explain_impact, axis=1)
    return result


if __name__ == "__main__":
    input_path = Path("data/AI_Business_Anomaly_Agent_Dataset.xlsx")
    output_path = Path("outputs/anomaly_report.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    results = prepare_results(input_path)
    results.to_csv(output_path, index=False)
    print(f"Saved {output_path}")
    print(f"Detected {int((results['severity'] != 'Normal').sum())} anomaly rows.")
