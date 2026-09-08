from __future__ import annotations

import os
from openai import OpenAI


def build_prompt(row) -> str:
    return f"""
You are a business data analyst.

Analyze the following detected business anomaly.

Date: {row['date'].date()}
Severity: {row['severity']}

Detected changes:
{row['ai_input']}

Business impact:
{row['business_impact']}

Write a concise analyst summary that:
1. States what changed.
2. Identifies the most important metric.
3. Explains the likely business implication.
4. Does not invent causes that are not supported by the data.
5. Ends with one recommended action.

Keep the response under 100 words.
"""


def generate_ai_summary(row, model: str = "gpt-5.6-luna") -> str:
    """Generate an analyst summary using the OpenAI Responses API."""
    if not os.getenv("OPENAI_API_KEY"):
        raise RuntimeError("OPENAI_API_KEY is not set.")

    client = OpenAI()
    response = client.responses.create(
        model=model,
        input=build_prompt(row),
    )
    return response.output_text.strip()
