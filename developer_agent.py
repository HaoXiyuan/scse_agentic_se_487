## The logic is fairly similar to the Analyst and Planner agents
import json
import re
from ollama import chat


SYSTEM_PROMPT = """
You are a software developer for a robot navigation system.

Output ONLY a single valid Python code block.
Do NOT include any explanation, comments, or extra text.
Do NOT wrap the code in ```python fences.

The code MUST define exactly this function:

def decide_next_move(state):
    ...

The input 'state' is a dictionary with these keys:
- goal_ahead (bool)
- goal_on_left (bool)
- goal_on_right (bool)
- front_blocked (bool)
- left_blocked (bool)
- right_blocked (bool)

Rules:
- Return exactly one of: "FORWARD", "LEFT", "RIGHT", "STOP".
- Never return a direction that is blocked.
- If goal_ahead is True and front is not blocked, return "FORWARD".
- If goal_on_left is True and left is not blocked, return "LEFT".
- If goal_on_right is True and right is not blocked, return "RIGHT".
- Otherwise, pick any unblocked direction.
- If all directions are blocked, return "STOP".
- All logic must be inside decide_next_move. No helper functions.
"""


def validate_code(data):
    if not isinstance(data, str):
        raise ValueError("Developer output is not a string.")

    if "def decide_next_move" not in data:
        raise ValueError("Generated code does not define 'decide_next_move'.")

    try:
        compile(data, "<generated>", "exec")
    except SyntaxError as e:
        raise ValueError(f"Generated code has a syntax error: {e}")

    print("=== Validation passed ===")
    print(data)
    print("=========================\n")


def extract_code(raw):
    """
    Extract the Python code from Qwen's response.
    Handles cases where Qwen adds explanation text or markdown fences.
    """
    match = re.search(r"```(?:python)?\s*(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()

    lines = raw.splitlines()
    start = None
    for i, line in enumerate(lines):
        if line.strip().startswith("def decide_next_move"):
            start = i
            break
    if start is not None:
        return "\n".join(lines[start:]).strip()

    return raw.strip()


def run_developer(plan):
    response = chat(
        model="qwen3:1.7b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": json.dumps(plan)},
        ],
    )

    raw = response.message.content
    print("=== Raw Qwen output ===")
    print(raw)
    print("=== End of raw output ===\n")

    cleaned = extract_code(raw)
    validate_code(cleaned)
    return cleaned