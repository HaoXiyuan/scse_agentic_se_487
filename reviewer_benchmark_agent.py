## Create a system prompt for the Reviewer Agent that instructs it to analyze the IR-SIM Benchmark report and output a JSON object with specific keys.
## The JSON object it outputs must follow a strict schema and contain keys "issue", "likely_cause", "recommendation", "safety_passed", "goal_completion_passed", "efficiency_passed", and "needs_revision".
## The Reviewer Agent should validate the output to ensure it adheres to the schema and that "safety_passed", "goal_completion_passed", "efficiency_passed", and "needs_revision" are booleans.



## Create a function to validate the output of the Reviewer Agent for the benchmark report.
## It should check that the output is a JSON object with the required keys and that "safety_passed", "goal_completion_passed", "efficiency_passed", and "needs_revision" are booleans, and the rest of the keys are strings.
## If the output does not meet these criteria, raise a ValueError.





## Create a function to build a deterministic review from the benchmark report.
## This function analyzes the benchmark report and determines the values for "safety_passed", "goal_completion_passed", "efficiency_passed", and "needs_revision" based on the measured benchmark fields.
## It returns a dictionary with the keys "issue", "likely_cause", "recommendation", "safety_passed", "goal_completion_passed", "efficiency_passed", and "needs_revision".
## If the benchmark report does not contain the required fields, default values will be used.
## If safety_passed is false, the issue will be described as "Unsafe benchmark behavior detected". Safety is measured as any world having collision_or_done true while reached_goal is false.
## If goal_completion_passed is false, the issue will be described as "Goal completion failure". Goal completion is measured as success_rate being less than 1.0.
## If efficiency_passed is false, the issue will be described as "Successful but inefficient navigation". Efficiency is measured as inefficient_success_worlds being greater than 0 or efficiency_rate being less than 1.0.





## Create a function to run the Reviewer Agent for the benchmark report.
## It should take in the benchmark report, build a deterministic review, send both to the Reviewer Agent, and return the validated output.
## The deterministic review is used to ensure that the pass/fail booleans in the output are based on the measured benchmark results, even if the LLM phrases the issue, likely cause, and recommendation.
## The output of this function will be a dictionary with the keys "issue", "likely_cause", "recommendation", "safety_passed", "goal_completion_passed", "efficiency_passed", and "needs_revision".

import json
from ollama import chat


# System prompt describing the Benchmark Reviewer Agent role and JSON schema
SYSTEM_PROMPT = """
You are a quality reviewer for a robot navigation benchmark.

You will receive an IR-SIM benchmark report and a deterministic review.

Output ONLY a single valid JSON object.
Do NOT include any explanation, markdown formatting, or extra text.

The JSON must have exactly these keys:
{
  "issue": "string",
  "likely_cause": "string",
  "recommendation": "string",
  "safety_passed": true,
  "goal_completion_passed": true,
  "efficiency_passed": true,
  "needs_revision": true
}

Rules:
- "issue" describes the main problem found in the benchmark.
- "likely_cause" explains why the problem likely occurred.
- "recommendation" suggests how to fix or improve.
- "safety_passed", "goal_completion_passed", "efficiency_passed",
  and "needs_revision" are booleans.
- The deterministic review provides the correct boolean values.
  You MUST use those boolean values verbatim.
"""


def validate_review(data):
    """Validate the Benchmark Reviewer Agent output against the required schema."""
    if not isinstance(data, dict):
        raise ValueError("Benchmark reviewer output is not a dictionary.")

    required = {
        "issue", "likely_cause", "recommendation",
        "safety_passed", "goal_completion_passed",
        "efficiency_passed", "needs_revision",
    }
    missing = required - data.keys()
    if missing:
        raise ValueError(f"Missing required keys: {missing}")

    extra = data.keys() - required
    if extra:
        raise ValueError(f"Unexpected extra keys: {extra}")

    for key in ("issue", "likely_cause", "recommendation"):
        if not isinstance(data[key], str):
            raise ValueError(f"'{key}' must be a string.")

    for key in ("safety_passed", "goal_completion_passed",
                "efficiency_passed", "needs_revision"):
        if not isinstance(data[key], bool):
            raise ValueError(f"'{key}' must be a boolean.")

    print("=== Benchmark reviewer validation passed ===")
    return True


def build_deterministic_review(benchmark_report):
    """Build a deterministic review from the measured benchmark fields."""
    success_rate = benchmark_report.get("success_rate", 0.0)
    efficiency_rate = benchmark_report.get("efficiency_rate", 0.0)
    inefficient_success = benchmark_report.get("inefficient_success_worlds", 0)

    # Safety fails if any world ended with collision_or_done but no goal
    unsafe = False
    for item in benchmark_report.get("results", []):
        report = item.get("report", {})
        if report.get("collision_or_done") and not report.get("reached_goal"):
            unsafe = True
            break
    safety_passed = not unsafe

    # Goal completion requires a perfect success rate
    goal_completion_passed = (success_rate >= 1.0)

    # Efficiency requires no inefficient successes and a perfect efficiency rate
    efficiency_passed = (inefficient_success == 0 and efficiency_rate >= 1.0)

    needs_revision = not (safety_passed and goal_completion_passed and efficiency_passed)

    # Build the issue text based on which check failed first
    if not safety_passed:
        issue = "Unsafe benchmark behavior detected"
        likely_cause = "Navigation logic produced collisions or terminal states before reaching the goal."
        recommendation = "Revise navigation logic to avoid blocked directions and ensure safe stops."
    elif not goal_completion_passed:
        issue = "Goal completion failure"
        likely_cause = "Navigation logic failed to reach the goal in one or more worlds."
        recommendation = "Improve goal-seeking behavior and fallback strategies."
    elif not efficiency_passed:
        issue = "Successful but inefficient navigation"
        likely_cause = "Navigation logic reached the goal but took too many steps."
        recommendation = "Optimize path selection to reduce step count."
    else:
        issue = "No issues detected"
        likely_cause = "N/A"
        recommendation = "No revision needed"

    return {
        "issue": issue,
        "likely_cause": likely_cause,
        "recommendation": recommendation,
        "safety_passed": safety_passed,
        "goal_completion_passed": goal_completion_passed,
        "efficiency_passed": efficiency_passed,
        "needs_revision": needs_revision,
    }


def extract_json(raw):
    """Extract JSON from the LLM response, stripping markdown fences."""
    cleaned = raw.strip()
    if cleaned.startswith("```"):
        cleaned = cleaned.split("```")[1]
        if cleaned.startswith("json"):
            cleaned = cleaned[4:]
    return cleaned.strip()


def run_reviewer_benchmark_agent(benchmark_report):
    """Run the Benchmark Reviewer Agent and return the validated review."""
    deterministic = build_deterministic_review(benchmark_report)

    user_content = json.dumps({
        "benchmark_report": benchmark_report,
        "deterministic_review": deterministic,
    })

    response = chat(
        model="qwen3:8b",
        messages=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    )

    raw = response.message.content
    print("=== Raw Benchmark Reviewer output ===")
    print(raw)
    print("=== End of raw output ===\n")

    data = json.loads(extract_json(raw))

    # Force the booleans to match the deterministic review
    for key in ("safety_passed", "goal_completion_passed",
                "efficiency_passed", "needs_revision"):
        data[key] = deterministic[key]

    validate_review(data)
    return data