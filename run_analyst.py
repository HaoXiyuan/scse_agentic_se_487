import json
from pathlib import Path

from analyst_agent import run_analyst


def main():
    # 1. Read the brief text
    brief = Path("brief.txt").read_text()

    # 2. Run the analyst agent to get validated requirements
    requirements = run_analyst(brief)

    # 3. Save the requirements as artifacts/requirements.json
    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)

    output_path = artifacts_dir / "requirements.json"
    with output_path.open("w") as file:
        json.dump(requirements, file, indent=2)

    print(f"Requirements saved to {output_path}")


if __name__ == "__main__":
    main()