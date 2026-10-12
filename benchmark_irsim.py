import json
import subprocess
import ast
import sys
import os
from pathlib import Path

## Load the world files for the IR-SIM benchmark.

## Create a function to run the IR-SIM benchmark for a given world file.
## It should call the test_irsim_with_agent.py script with the world file as an argument, capture the output, and extract the report from the output.




## Create a main function to run the IR-SIM benchmark for all world files and generate a summary report.
## The summary report should include the total number of worlds, the number of worlds where the goal was reached, the success rate, the number of efficient worlds, the number of inefficient but successful worlds, the number of failed worlds, the efficiency rate, and the average steps taken across all worlds. The report should be saved to a JSON file.
## The benchmark report must have the following structure:
""" benchmark_report = {
        "total_worlds": total,
        "goals_reached": reached_goal_count,
        "success_rate": reached_goal_count / total,
        "efficient_worlds": efficient_count,
        "inefficient_success_worlds": inefficient_success_count,
        "failed_worlds": failed_count,
        "efficiency_rate": efficient_count / total,
        "average_steps_taken": average_steps,
        "results": results
    } """
## Save the benchmark report to a JSON file named "irsim_benchmark_report.json" under the artifacts folder, and print the report to the console in a readable format.

# Use a non-interactive matplotlib backend so the simulation does not block
os.environ["MPLBACKEND"] = "Agg"

# The four IR-SIM worlds to benchmark, in order of difficulty
WORLD_FILES = [
    "irsim_worlds/world_easy.yaml",
    "irsim_worlds/world_medium.yaml",
    "irsim_worlds/world_hard.yaml",
    "irsim_worlds/world_custom.yaml",
]


def extract_report_from_output(output):
    marker = "IR-SIM report:"
    if marker not in output:
        raise ValueError("Could not find 'IR-SIM report:' in output.")

    after = output.split(marker, 1)[1].strip()
    first_line = after.splitlines()[0].strip()
    try:
        report = ast.literal_eval(first_line)
    except Exception:
        report = None

    if report is None:
        p = Path("artifacts/irsim_report.json")
        if p.exists():
            report = json.loads(p.read_text())
        else:
            raise ValueError("Could not extract IR-SIM report.")

    return report


def run_irsim_benchmark(world_file):
    print(f"\n=== Running IR-SIM for {world_file} ===")
    result = subprocess.run(
        [sys.executable, "test_irsim_with_agent.py", world_file],
        capture_output=True,
        text=True,
        timeout=120,
    )

    output = result.stdout + "\n" + result.stderr
    print(output)

    report = extract_report_from_output(output)
    return report


def main():
    results = []
    reached_goal_count = 0
    efficient_count = 0
    inefficient_success_count = 0
    failed_count = 0
    total_steps = 0

    for world in WORLD_FILES:
        try:
            report = run_irsim_benchmark(world)
        except Exception as e:
            print(f"ERROR running {world}: {e}")
            report = {
                "reached_goal": False,
                "collision_or_done": True,
                "steps_taken": 0,
                "efficiency_status": "failed",
                "efficiency_passed": False,
            }

        results.append({"world": world, "report": report})

        steps = report.get("steps_taken", 0)
        total_steps += steps

        if report.get("reached_goal"):
            reached_goal_count += 1
            if report.get("efficiency_passed"):
                efficient_count += 1
            else:
                inefficient_success_count += 1
        else:
            failed_count += 1

    total = len(WORLD_FILES)

    benchmark_report = {
        "total_worlds": total,
        "goals_reached": reached_goal_count,
        "success_rate": reached_goal_count / total if total else 0.0,
        "efficient_worlds": efficient_count,
        "inefficient_success_worlds": inefficient_success_count,
        "failed_worlds": failed_count,
        "efficiency_rate": efficient_count / total if total else 0.0,
        "average_steps_taken": total_steps / total if total else 0.0,
        "results": results,
    }

    artifacts_dir = Path("artifacts")
    artifacts_dir.mkdir(exist_ok=True)
    out = artifacts_dir / "irsim_benchmark_report.json"
    out.write_text(json.dumps(benchmark_report, indent=2))

    print("\n=== IR-SIM Benchmark Report ===")
    print(json.dumps(benchmark_report, indent=2))
    print(f"Saved to {out}")
    return benchmark_report


if __name__ == "__main__":
    main()