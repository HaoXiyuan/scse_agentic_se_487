from ollama import chat

response = chat(
    model="qwen3:8b",
    messages=[
        {
            "role": "user",
            "content": "Reply with exactly: Python can talk to Qwen."
        }
    ]
)
print(response.message.content)