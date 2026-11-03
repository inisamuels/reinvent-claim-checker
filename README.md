# reinvent-claim-checker

A small script that fact-checks a claim from a CSV. It looks up a claim by ID, sends the record to a Claude model through OpenRouter, and prints a JSON verdict (`supported`, `refuted`, or `unverifiable`) with a short rationale. Each run is traced in LangSmith.

## Example trace

Public LangSmith trace of the C-02 run: https://smith.langchain.com/public/dd111d5b-deda-45db-a3d7-cce74f8c4648/r/01a1a2f0-f2b8-7f94-9482-ff3ea44b9d33?start_time=2026-11-03T19%3A44%3A22.200345Z&scroll_to=metadata

## Baseline result for C-02 (before)

This records what the model said with no web access, before any grounding is added.

**Model:** `anthropic/claude-opus-5.5` via OpenRouter, `temperature=0`

**Verdict:** `unverifiable`

**Rationale (verbatim from the run):**

> The claim predicts an announcement at re:Invent 2025, which had not happened when the record was collected (2025-10-31), and the only source is the generic Hacker News front-page URL, not a specific article or any official AWS statement. The claim is also internally implausible: us-east-1 (N. Virginia) is already an existing AWS Region, so a new 'quantum Region' could not launch there, and AWS already offers managed quantum computing through Amazon Braket, which is available in us-east-1. With no authoritative evidence and a premise that conflicts with how AWS structures Regions, the claim cannot be confirmed and should be treated with strong skepticism.

**Did the model name an aws.amazon.com page?** No. It cited no aws.amazon.com URL. It referred to Amazon Braket by name and pointed out that the record's only source was the Hacker News front page, but it gave no official AWS page to back anything up.

## Setup

1. Clone the repo and enter it:
   ```
   git clone <your-repo-url>
   cd reinvent-claim-checker
   ```
2. Install dependencies (Python 3.9+):
   ```
   pip3 install -r requirements.txt
   ```
3. Copy the template and fill in your own values:
   ```
   cp .env.example .env
   ```
   - `OPENROUTER_API_KEY`: your OpenRouter key
   - `LANGSMITH_API_KEY`: your LangSmith key
   - `LANGSMITH_TRACING=true`
   - `LANGSMITH_PROJECT=reinvent-claim-checker`
   - `CLAUDE_MODEL_ID`: the `anthropic/...` model slug from openrouter.ai/models
4. Put the claims CSV in `data/`.

## Run

```
python3 check_claim.py C-02
```

Output is JSON with `verdict` and `rationale`. The run appears in the `reinvent-claim-checker` project in LangSmith as a `check_claim` trace with the model call nested inside.

## How it works

- Finds the row containing the given claim ID in any CSV in `data/`.
- Sends the row to the model via OpenRouter's OpenAI-compatible API (`max_tokens=500`, `temperature=0`).
- Parses the model's JSON reply. If it isn't valid JSON, the verdict is `unparsed` and the raw text is returned.
- The LangSmith `@traceable` decorator and OpenAI wrapper record the run.

## Security

No API keys are committed. `.env` is listed in `.gitignore`, and `.env.example` contains blank values only.

## Limitations

The model only sees the CSV row and its own knowledge. It does not search the web, so verdicts on recent or obscure claims are often `unverifiable`.