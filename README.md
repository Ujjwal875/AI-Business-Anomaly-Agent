# AI Business Anomaly Monitoring Agent

An AI-powered business analytics project that reads daily business metrics, detects unusual movements against a recent baseline, classifies severity, explains business impact, and prepares concise analyst-style summaries.

## Problem
Business teams often need to notice unusual changes in revenue, orders, traffic, conversion, costs, and refunds quickly. A manual spreadsheet review can miss important movements.

## Solution
This project turns a business-metrics Excel file into an automated anomaly-monitoring workflow:

1. Read business data from Excel
2. Validate and clean the dataset
3. Calculate rolling recent baselines
4. Measure percentage deviation from baseline
5. Flag significant anomalies using a configurable threshold
6. Classify anomaly severity
7. Explain the potential business impact
8. Prepare structured input for an LLM
9. Generate a concise business-friendly analyst summary
10. Produce an anomaly report and alerts

## Dataset
The project uses daily business metrics with these fields:

- `date`
- `revenue`
- `orders`
- `conversion_rate`
- `traffic`
- `cost`
- `refunds`

The working dataset contains 90 daily records and was designed with intentional unusual movements for testing anomaly detection.

## Anomaly Detection
The current prototype compares each metric with a recent rolling baseline and calculates percentage deviation. A configurable threshold is used to flag unusual movements.

Severity is based on the largest absolute deviation:

- **Normal:** below 20%
- **Medium:** 20%–29.9%
- **High:** 30%–49.9%
- **Critical:** 50% or more

An unusual movement is not automatically treated as negative. For example, a reduction in refunds may be unusual but potentially positive, so the business-impact layer considers metric direction and context.

## AI Layer
For detected anomalies, the system prepares structured metric, baseline, deviation, severity, and impact information for an LLM. The model is instructed to:

- state what changed
- identify the most important metric
- explain the likely business implication without inventing unsupported causes
- recommend one action
- keep the summary concise

## Tech Stack
- Python
- Pandas
- Excel / OpenPyXL
- Statistical baseline comparison
- LLM API
- Jupyter / Google Colab
- GitHub

## Project Structure
```text
AI-Business-Anomaly-Agent/
├── README.md
├── requirements.txt
├── .gitignore
├── data/
│   └── README.md
├── notebooks/
│   └── anomaly_agent.ipynb
└── src/
    ├── anomaly_detector.py
    └── ai_summary.py
```

## Example Detection
A test anomaly can look like:

```text
Date: 2026-06-08
Severity: High
Metric: refunds
Current value: 9526
Recent baseline: 15781
Deviation: -39.6%
```

The system recognizes the movement as unusual and passes the structured context to the AI layer for business interpretation.

## Future Improvements
- Automated email alerts
- Streamlit dashboard
- Historical alert log
- Configurable thresholds through a UI
- Multiple baseline strategies
- Trend and seasonality detection
- Deployment as a scheduled monitoring service

## Portfolio Value
This project demonstrates practical skills in data cleaning, exploratory analysis, anomaly detection, business reasoning, Python automation, and LLM integration rather than only a static EDA notebook.