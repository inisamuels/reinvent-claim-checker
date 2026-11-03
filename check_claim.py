import csv
import json
import os
import sys

from dotenv import load_dotenv
from langsmith import traceable
from langsmith.wrappers import wrap_openai
from openai import OpenAI

load_dotenv()

client = wrap_openai(
    OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=os.environ["OPENROUTER_API_KEY"],
    )
)
MODEL = os.environ["CLAUDE_MODEL_ID"]


def load_row(claim_id):
    """Find the row containing claim_id in any CSV inside data/."""
    for name in sorted(os.listdir("data")):
        if not name.lower().endswith(".csv"):
            continue
        with open(os.path.join("data", name), newline="", encoding="utf-8-sig") as f:
            for row in csv.DictReader(f):
                if claim_id in [str(v).strip() for v in row.values()]:
                    return row
    return None


@traceable(name="check_claim")
def check_claim(claim_id):
    row = load_row(claim_id)
    if row is None:
        raise SystemExit(f"No row containing '{claim_id}' found in data/*.csv")

    prompt = (
        "You are a careful fact-checker. Here is one claim record as JSON:\n\n"
        f"{json.dumps(row, ensure_ascii=False, indent=2)}\n\n"
        "Assess the claim using only what is in the record and your own knowledge. "
        'Reply with JSON only, in this shape: {"verdict": "supported" | "refuted" | '
        '"unverifiable", "rationale": "<2-4 sentences>"}'
    )
    resp = client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
        temperature=0,
        max_tokens=500,
    )
    text = resp.choices[0].message.content.strip()
    text = text.removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    try:
        return json.loads(text)
    except json.JSONDecodeError:
        return {"verdict": "unparsed", "rationale": text}


if __name__ == "__main__":
    if len(sys.argv) != 2:
        raise SystemExit("Usage: python3 check_claim.py <CLAIM_ID>, e.g. C-02")
    print(json.dumps(check_claim(sys.argv[1]), indent=2, ensure_ascii=False))