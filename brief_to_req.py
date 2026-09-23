from pathlib import Path
from ollama import chat

# 1. Read the brief text
brief = Path("brief.txt").read_text()
print("=== Brief loaded ===")
print(brief)
print("=== End of brief ===\n")

# 2. Ask Qwen to convert the brief into software requirements
prompt = f"""
You are a requirements engineer.
Read the following brief and convert it into clear software requirements.

Brief:
{brief}
"""

response = chat(
    model="qwen3:8b",
    messages=[
        {"role": "user", "content": prompt}
    ]
)

requirements = response.message.content
print("=== Qwen output ===")
print(requirements)
print("=== End of output ===\n")

# 3. Save the output to robot_requirements.txt
Path("robot_requirements.txt").write_text(requirements)
print("Saved to robot_requirements.txt")