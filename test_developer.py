import json
from pathlib import Path

from developer_agent import run_developer


def main():
    # 1. Read the plan from plan.json
    plan_path = Path("artifacts") / "plan.json"
    with plan_path.open("r") as file:
        plan = json.load(file)

    # 2. Run the developer agent
    code = run_developer(plan)

    # 3. Save to artifacts/navigation_logic.py
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    output_path = artifacts_dir / "navigation_logic.py"
    output_path.write_text(code)

    # 4. Display the result
    print("=== Test result: navigation_logic.py ===")
    print(code)
    print("========================================")


if __name__ == "__main__":
    main()