import json
from pathlib import Path

from planner_agent import run_planner


def main():
    # 1. Read the requirements from requirements.json
    requirements_path = Path("artifacts") / "requirements.json"
    with requirements_path.open("r") as file:
        requirements = json.load(file)

    # 2. Run the planner agent
    plan = run_planner(requirements)

    # 3. Save to artifacts/plan.json
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    output_path = artifacts_dir / "plan.json"
    with output_path.open("w") as file:
        json.dump(plan, file, indent=2)

    # 4. Display the result
    print("=== Test result: plan.json ===")
    print(json.dumps(plan, indent=2))
    print("==============================")


if __name__ == "__main__":
    main()