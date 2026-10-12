## Create a system prompt for the Reviewer Agent that instructs it to analyze the simulation report and output a JSON object with specific keys.
## The JSON object it outputs must follow a strict schema and contain keys "issue", "likely_cause", "recommendation", and "needs_revision".
## The Reviewer Agent should validate the output to ensure it adheres to the schema and that "needs_revision" is a boolean.


## Create a function to validate the output of the Reviewer Agent.
## It should check that the output is a JSON object with the required keys and that "needs_revision" is a boolean, and the rest of the keys are strings.


## Create a function to run the Reviewer Agent.
## It should take in the simulation report, send it to the Reviewer Agent, and return the validated output.

import json
from ollama import chat


# System prompt describing the Reviewer Agent role and JSON schema
SYSTEM_PROMPT = """
You are a code reviewer for a robot navigation system.

You will receive a simulation report that summarises how the
`decide_next_move` function performed against a set of scenarios.

Output ONLY a single valid JSON object.
Do NOT include any explanation, markdown formatting, or extra text.

The JSON must have exactly these keys:
{
  "issue": "string",
  "likely_cause": "string",
  "recommendation": "string",
  "needs_revision": true
}

Rules:
- "issue" describes the main problem found in the simulation report.
- "likely_cause" explains why the problem likely occurred.
- "recommendation" suggests how to fix or improve the navigation logic.
- "needs_revision" is a boolean: true if the navigation logic should be revised.
- If there are no failures, set "issue" to "No issues detected",
  "likely_cause" to "N/A", "recommendation" to "No revision needed",
  and "needs_revision" to false.
"""


def validate_review(data):
    """Validate the Reviewer Agent output against the required schema."""
    if not isinstance(data, dict):
        raise ValueError("Reviewer output is not a dictionary.")

    required = {"issue", "likely_cause", "recommendation", "needs_revision"}
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    extra = data.keys() - required
    if extra:
        raise ValueError(f"Unexpected extra keys: {extra}")

    for key in ("issue", "likely_cause", "recommendation"):
        if not isinstance(data[key], str):
            raise ValueError(f"'{key}' must be a string.")

    if not isinstance(data["needs_revision"], bool):
        raise ValueError("'needs_revision' must be a boolean.")

    print("=== Reviewer validation passed ===")
    return True


def extract_json(raw):
    """Extract JSON from the LLM response, stripping markdown fences."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return cleaned.strip()


def run_reviewer_agent(simulation_report):
    """Run the Reviewer Agent on the simulation report and return the validated review."""
    user_content = json.dumps(simulation_report)

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )

    raw = response.message.content
    print("=== Raw Reviewer output ===")
    print(raw)
    print("=== End of raw output ===\n")

    data = json.loads(extract_json(raw))
    validate_review(data)
    return data