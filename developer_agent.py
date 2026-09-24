## The logic is fairly similar to the Analyst and Planner agents
import json
from ollama import chat


SYSTEM_PROMPT = """
You are a software developer for a robot navigation system.
Your job is to take a validated navigation plan and write the Python code that implements it.

You must output ONLY a single valid Python code block.
Do not include any explanation, markdown formatting, or extra text.
Do NOT wrap the code in ```python ... ``` fences.

The code MUST define a function with this exact signature:

def decide_action(front_blocked, left_blocked, right_blocked, goal_direction):
    ...

Rules:
- front_blocked, left_blocked, right_blocked are booleans (True means blocked).
- goal_direction is one of: "ahead", "left", "right".
- Handle all three goal_direction values: "ahead", "left", "right".
- The function must return one of: "FORWARD", "LEFT", "RIGHT", "STOP".
- Never return a direction that is blocked.
- Prefer moving toward the goal if that direction is unblocked.
- If no safe direction is available, return "STOP".
"""


def validate_code(data):
    if not isinstance(data, str):
        raise ValueError("Developer output is not a string.")

    if "def decide_action" not in data:
        raise ValueError("Generated code does not define 'decide_action'.")

    try:
        compile(data, "<generated>", "exec")
    except SyntaxError as e:
        raise ValueError(f"Generated code has a syntax error: {e}")

    print("=== Validation passed ===")
    print(data)
    print("=========================\n")


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

    # Clean possible markdown code fences like ```python ... ```
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("python"):
            cleaned = cleaned[6:]
    cleaned = cleaned.strip()

    validate_code(cleaned)
    return cleaned