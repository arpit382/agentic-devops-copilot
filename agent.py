import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()

client = Groq(api_key=os.getenv("GROQ_API_KEY"))

def read_recent_logs(filepath="app_logs.txt", n=20):
    with open(filepath, "r") as f:
        lines = f.readlines()
    return "".join(lines[-n:])

def diagnose(logs):
    prompt = f"""You are a DevOps AI agent monitoring an application's logs.
Analyze the following recent logs and:
1. Identify if there is a problem (yes/no)
2. If yes, explain what's failing and likely cause
3. Recommend one concrete action to take

Logs:
{logs}
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
    )
    return response.choices[0].message.content

if __name__ == "__main__":
    logs = read_recent_logs()
    print("=== Recent Logs ===")
    print(logs)
    print("=== Agent Diagnosis ===")
    diagnosis = diagnose(logs)
    print(diagnosis)