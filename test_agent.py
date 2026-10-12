### Create a system prompt that instructs the Test Agent to generate pytest-style tests for the decide_next_move function,
# based on the requirements and plan provided.
# The prompt should specify the expected input structure and required test coverage,
# while also enforcing constraints on the output format.


## Write a function to validate the generated test code.
# It should check that the code is a non-empty string, does not contain markdown fences,
# Also check that the test code includes all the necessary keywords like the import statements and test assertions.


## Write a function to run the Test Agent.
# It should take in requirements and a plan, send them to the Test Agent.
# Thefunction must return the generated test code after validation.

import json
import re
from ollama import chat


# System prompt that describes the Test Agent role and output constraints
SYSTEM_PROMPT = """
You are a test engineer for a robot navigation system.

Your job is to write pytest-style tests for the function `decide_next_move(state)`.

Output ONLY valid Python code.
Do NOT wrap the code in markdown fences.
Do NOT include any explanation text.

The function under test:
    def decide_next_move(state): ...

The input `state` is a dict with these keys (all bool):
- goal_ahead
- goal_on_left
- goal_on_right
- front_blocked
- left_blocked
- right_blocked

The function returns exactly one of: "FORWARD", "LEFT", "RIGHT", "STOP".

Rules:
- The test file MUST import: from generated.navigation_logic import decide_next_move
- The test file MUST define at least one function whose name starts with `test_`.
- The test file MUST contain `assert` statements.
- Cover ALL possible scenarios:
  * goal ahead and front clear -> FORWARD
  * goal on left and left clear -> LEFT
  * goal on right and right clear -> RIGHT
  * goal direction blocked, fallback to another unblocked direction
  * all directions blocked -> STOP
  * no goal direction indicated but front clear -> FORWARD
- Every returned action must be one of the four valid actions.

Return only the Python test code.
"""


def validate_test_code(code):
    """Validate the generated test code before returning it."""
    # The output must be a non-empty string
    if not isinstance(code, str) or not code.strip():
        raise ValueError("Test agent output is empty.")

    # Markdown fences are not allowed
    if "```" in code:
        raise ValueError("Test agent output contains markdown fences.")

    # The required import must be present
    if "from generated.navigation_logic import decide_next_move" not in code:
        raise ValueError("Test code missing required import.")

    # At least one test function must be defined
    if "def test_" not in code:
        raise ValueError("Test code does not define any test function.")

    # Assertions must be present
    if "assert" not in code:
        raise ValueError("Test code does not contain assert statements.")

    # The code must be syntactically valid Python
    try:
        compile(code, "<generated_test>", "exec")
    except SyntaxError as e:
        raise ValueError(f"Test code has a syntax error: {e}")

    print("=== Test code validation passed ===")
    return True


def extract_code(raw):
    """Extract Python code from the LLM response, stripping markdown fences."""
    match = re.search(r"```(?:python)?\s*(.*?)```", raw, re.DOTALL)
    if match:
        return match.group(1).strip()
    return raw.strip()


def run_test_agent(requirements, plan):
    """Run the Test Agent and return the validated test code."""
    user_content = json.dumps({
        "requirements": requirements,
        "plan": plan,
    })

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )

    raw = response.message.content
    print("=== Raw Test Agent output ===")
    print(raw)
    print("=== End of raw output ===\n")

    code = extract_code(raw)
    validate_test_code(code)
    return code