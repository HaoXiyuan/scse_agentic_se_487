import json
import os
import subprocess
import sys


## Import all the necessary functions from other modules to run the entire pipeline.



## Write a main function to run the entire pipeline.
## It should create necessary directories, or check that it exists,
# Then run each agent in sequence, save their outputs to files, and log events.
# Logging events should include the name of the agent and the action taken, such as "Analyst Agent created requirements.json".

from pathlib import Path

from analyst_agent import run_analyst
from planner_agent import run_planner
from developer_agent import run_developer, run_developer_revision
from test_agent import run_test_agent
from runner import run_simulation
from reviewer_agent import run_reviewer_agent
from benchmark_irsim import main as run_benchmark
from reviewer_benchmark_agent import run_reviewer_benchmark_agent


ARTIFACTS = Path("artifacts")
GENERATED = Path("generated")
TRACE = Path("trace.log")


def log(event):
    """Append a timestamped event to trace.log and print it."""
    print(f"[TRACE] {event}")
    with TRACE.open("a", encoding="utf-8") as f:
        f.write(event + "\n")


def main():
    """Run the entire pipeline in sequence."""
    # Make sure the required directories exist
    ARTIFACTS.mkdir(exist_ok=True)
    GENERATED.mkdir(exist_ok=True)
    (GENERATED / "__init__.py").touch(exist_ok=True)

    # Reset the trace log at the start of each run
    TRACE.write_text("", encoding="utf-8")

    # 1. Load the brief
    brief = Path("brief.txt").read_text(encoding="utf-8")
    log("Loaded brief.txt")

    # 2. Run the Analyst agent
    requirements = run_analyst(brief)
    (ARTIFACTS / "requirements.json").write_text(
        json.dumps(requirements, indent=2), encoding="utf-8")
    log("Analyst Agent created requirements.json")

    # 3. Run the Planner agent
    plan = run_planner(requirements)
    (ARTIFACTS / "plan.json").write_text(
        json.dumps(plan, indent=2), encoding="utf-8")
    log("Planner Agent created plan.json")

    # 4. Run the Developer agent
    code = run_developer(plan)
    nav_path = GENERATED / "navigation_logic.py"
    nav_path.write_text(code, encoding="utf-8")
    log("Developer Agent created generated/navigation_logic.py")

    # 5. Run the Test agent
    test_code = run_test_agent(requirements, plan)
    test_path = ARTIFACTS / "test_generated_navigation_logic.py"
    test_path.write_text(test_code, encoding="utf-8")
    log("Test Agent created artifacts/test_generated_navigation_logic.py")

    # 6. Run the simulation
    sim_report = run_simulation()
    (ARTIFACTS / "simulation_report.json").write_text(
        json.dumps(sim_report, indent=2), encoding="utf-8")
    log("Simulation Runner created simulation_report.json")

    # 7. Run the Reviewer agent
    review = run_reviewer_agent(sim_report)
    (ARTIFACTS / "simulation_review.json").write_text(
        json.dumps(review, indent=2), encoding="utf-8")
    log("Reviewer Agent created simulation_review.json")

    # 8. Run the IR-SIM benchmark
    benchmark_report = run_benchmark()
    log("IR-SIM Benchmark created irsim_benchmark_report.json")

    # 9. Run the Benchmark Reviewer
    benchmark_review = run_reviewer_benchmark_agent(benchmark_report)
    (ARTIFACTS / "benchmark_review.json").write_text(
        json.dumps(benchmark_review, indent=2), encoding="utf-8")
    log("Benchmark Reviewer created benchmark_review.json")

    # 10. Revise the navigation logic if any reviewer requested it
    if benchmark_review.get("needs_revision") or review.get("needs_revision"):
        log("Revision required. Running developer revision...")
        original_code = nav_path.read_text(encoding="utf-8")
        revised = run_developer_revision(
            original_code,
            review,
            benchmark_report,
            requirements,
            plan,
        )
        nav_path.write_text(revised, encoding="utf-8")
        log("Developer revision created new navigation_logic.py")

        # Re-run simulation and benchmark after the revision
        sim_report2 = run_simulation()
        (ARTIFACTS / "simulation_report.json").write_text(
            json.dumps(sim_report2, indent=2), encoding="utf-8")
        log("Re-ran simulation after revision")

        run_benchmark()
        log("Re-ran IR-SIM benchmark after revision")
    else:
        log("No revision required.")

    log("Pipeline finished.")


if __name__ == "__main__":
    main()