import json
from pathlib import Path

from analyst_agent import run_analyst


def main():
    # 1. Read the brief text
    brief = Path("brief.txt").read_text()

    # 2. Run the analyst agent
    requirements = run_analyst(brief)

    # 3. Save to artifacts/requirements.json
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    output_path = artifacts_dir / "requirements.json"
    with output_path.open("w") as file:
        json.dump(requirements, file, indent=2)

    # 4. Display the result
    print("=== Test result: requirements.json ===")
    print(json.dumps(requirements, indent=2))
    print("=====================================")


if __name__ == "__main__":
    main()