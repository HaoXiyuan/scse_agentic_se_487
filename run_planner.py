import json
from pathlib import Path

from planner_agent import run_planner


## Create a function/logic that reads the requirements from requirements.json, 
# then calls the run_planner function with the requirements as input, and finally writes the validated plan to plan.json.
def main():
    # 1. Read the requirements from requirements.json
    requirements_path = Path("artifacts") / "requirements.json"
    with requirements_path.open("r") as file:
        requirements = json.load(file)

    # 2. Run the planner agent to get validated plan
    plan = run_planner(requirements)

    # 3. Save the plan as artifacts/plan.json
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    output_path = artifacts_dir / "plan.json"
    with output_path.open("w") as file:
        json.dump(plan, file, indent=2)

    print(f"Plan saved to {output_path}")


if __name__ == "__main__":
    main()