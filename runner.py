## Create a function to run the simulation of the navigation logic.
## It should define a set of scenarios with different states (e.g., front_blocked, left_blocked, right_blocked), expected outputs (e.g., FORWARD, LEFT, RIGHT, STOP), and then run the decide_next_move function on each scenario.
## The function should collect the results, including whether the actual output matches the expected output, and return a report summarizing the results.
## The report must include the total number of scenarios, the number of passed and failed scenarios, and a success rate, which is the number of passed scenarios divided by the total number of scenarios.


## If this script is run directly, run the simulation function and save the simulation report to a JSON file.

import json
from pathlib import Path

from generated.navigation_logic import decide_next_move


# All possible scenarios to cover the navigation logic
SCENARIOS = [
    # Goal ahead, front clear -> FORWARD
    ({"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": False, "left_blocked": False, "right_blocked": False},
     "FORWARD"),

    # Goal on left, left clear -> LEFT
    ({"goal_ahead": False, "goal_on_left": True, "goal_on_right": False,
      "front_blocked": False, "left_blocked": False, "right_blocked": False},
     "LEFT"),

    # Goal on right, right clear -> RIGHT
    ({"goal_ahead": False, "goal_on_left": False, "goal_on_right": True,
      "front_blocked": False, "left_blocked": False, "right_blocked": False},
     "RIGHT"),

    # Goal ahead but front blocked, left clear -> LEFT
    ({"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": True, "left_blocked": False, "right_blocked": False},
     "LEFT"),

    # Goal ahead, front and left blocked, right clear -> RIGHT
    ({"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": True, "left_blocked": True, "right_blocked": False},
     "RIGHT"),

    # All directions blocked -> STOP
    ({"goal_ahead": True, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": True, "left_blocked": True, "right_blocked": True},
     "STOP"),

    # No goal direction but front clear -> FORWARD (fallback)
    ({"goal_ahead": False, "goal_on_left": False, "goal_on_right": False,
      "front_blocked": False, "left_blocked": False, "right_blocked": False},
     "FORWARD"),

    # Goal on left but left blocked, front clear -> FORWARD (fallback)
    ({"goal_ahead": False, "goal_on_left": True, "goal_on_right": False,
      "front_blocked": False, "left_blocked": True, "right_blocked": False},
     "FORWARD"),

    # Goal on right but right blocked, front clear -> FORWARD (fallback)
    ({"goal_ahead": False, "goal_on_left": False, "goal_on_right": True,
      "front_blocked": False, "left_blocked": False, "right_blocked": True},
     "FORWARD"),
]


def run_simulation():
    """Run all scenarios and return a report summarizing the results."""
    results = []
    passed = 0
    failed = 0

    for state, expected in SCENARIOS:
        try:
            actual = decide_next_move(state)
        except Exception as e:
            actual = f"ERROR: {e}"

        ok = (actual == expected)
        if ok:
            passed += 1
        else:
            failed += 1

        results.append({
            "state": state,
            "expected": expected,
            "actual": actual,
            "passed": ok,
        })

    total = len(SCENARIOS)
    report = {
        "total_scenarios": total,
        "passed": passed,
        "failed": failed,
        "success_rate": passed / total if total else 0.0,
        "results": results,
    }

    print("=== Simulation report ===")
    print(json.dumps(report, indent=2))
    print("=========================")
    return report


if __name__ == "__main__":
    report = run_simulation()
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    out = artifacts_dir / "simulation_report.json"
    out.write_text(json.dumps(report, indent=2))
    print(f"Simulation report saved to {out}")