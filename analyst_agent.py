import json
from ollama import chat


# System prompt: defines the role, rules, and required output structure
SYSTEM_PROMPT = """
You are a requirements engineer.
Your job is to analyze a brief text and convert it into explicit software requirements.

You must output ONLY a single valid JSON object.
Do not include any explanation, markdown formatting, or extra text.

The JSON must have exactly these keys:
{
  "goal": "string",
  "allowed actions": ["FORWARD", "LEFT", "RIGHT", "STOP"],
  "safe stop": true,
  "avoid obstacles": true
}

Rules:
- "goal" stores the navigation objective as a string.
- "allowed actions" are the valid steps the robot can take.
  It must ONLY contain: FORWARD, LEFT, RIGHT, STOP. No other actions.
- "safe stop" is a boolean: whether the robot should stop safely when it cannot go anywhere.
- "avoid obstacles" is a boolean: whether the robot must avoid anything blocking its path.
"""


def run_analyst(brief_text):
    """
    Send the brief text to Qwen and return validated requirements as a Python dict.
    """
    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": brief_text},
        ],
    )

    raw = response.message.content
    print("=== Raw Qwen output ===")
    print(raw)
    print("=== End of raw output ===\n")

    # Clean possible markdown code fences like ```json ... ```
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    cleaned = cleaned.strip()

    # Convert JSON text into a Python data structure
    data = json.loads(cleaned)

    # Validate the data
    validate_requirements(data)

    return data


def validate_requirements(data):
    """
    Validate that the data is a dictionary with the exact required keys and types.
    Raises an exception if anything is wrong.
    """
    # Must be a dictionary
    if not isinstance(data, dict):
        raise ValueError("Qwen output is not a dictionary.")

    required_keys = {"goal", "allowed actions", "safe stop", "avoid obstacles"}

    # Must have all required keys
    missing = required_keys - data.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    # Must not have extra keys
    extra = data.keys() - required_keys
    if extra:
        raise ValueError(f"Unexpected extra keys: {extra}")

    # Type checks
    if not isinstance(data["goal"], str):
        raise ValueError("'goal' must be a string.")

    if not isinstance(data["allowed actions"], list):
        raise ValueError("'allowed actions' must be a list.")

    allowed = {"FORWARD", "LEFT", "RIGHT", "STOP"}
    if not set(data["allowed actions"]).issubset(allowed):
        raise ValueError(
            f"'allowed actions' contains invalid actions: "
            f"{set(data['allowed actions']) - allowed}"
        )

    if not isinstance(data["safe stop"], bool):
        raise ValueError("'safe stop' must be a boolean.")

    if not isinstance(data["avoid obstacles"], bool):
        raise ValueError("'avoid obstacles' must be a boolean.")

    print("=== Validation passed ===")
    print(data)
    print("=========================\n")


if __name__ == "__main__":
    # Quick test: run the analyst on the brief directly
    from pathlib import Path

    brief = Path("brief.txt").read_text()
    result = run_analyst(brief)
    print("Final result:")
    print(result)