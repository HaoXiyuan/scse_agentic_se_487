## the logic is similar to the run_planner and run_analyst files
import json
from pathlib import Path

from developer_agent import run_developer


def main():
    plan_path = Path("artifacts") / "plan.json"
    with plan_path.open("r") as file:
        plan = json.load(file)

    code = run_developer(plan)

    output_path = Path("artifacts") / "navigation_logic.py"
    output_path.write_text(code)

    print(f"Navigation logic saved to {output_path}")


if __name__ == "__main__":
    main()