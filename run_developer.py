## the logic is similar to the run_planner and run_analyst files
import json
from pathlib import Path

from developer_agent import run_developer


def main():
    plan_path = Path("artifacts") / "plan.json"
    with plan_path.open("r") as file:
        plan = json.load(file)

    code = run_developer(plan)

    # Save the generated navigation logic into the generated/ package
    output_path = Path("generated") / "navigation_logic.py"
    output_path.parent.mkdir(exist_ok=True)
    output_path.write_text(code)

    print(f"Navigation logic saved to {output_path}")


if __name__ == "__main__":
    main()