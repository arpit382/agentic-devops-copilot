import os
import subprocess
import json
from datetime import datetime
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
Analyze the following recent logs and respond ONLY in this exact JSON format, nothing else:
{{
  "problem_detected": true or false,
  "explanation": "short explanation of the issue and likely cause",
  "recommended_action": "restart_service" or "no_action"
}}

Logs:
{logs}
"""
    response = client.chat.completions.create(
        model="openai/gpt-oss-20b",
        messages=[{"role": "user", "content": prompt}],
    )
    content = response.choices[0].message.content
    # Extract JSON even if wrapped in extra text
    start = content.find("{")
    end = content.rfind("}") + 1
    return json.loads(content[start:end])

def take_action(decision):
    action_log = {
        "timestamp": datetime.now().isoformat(),
        "problem_detected": decision["problem_detected"],
        "explanation": decision["explanation"],
        "action_taken": decision["recommended_action"]
    }

    if decision["recommended_action"] == "restart_service":
        print(">>> Agent decided to restart the service container...")
        subprocess.run(["docker", "restart", "devops-agent-container"])
        action_log["result"] = "container restarted"
    else:
        action_log["result"] = "no action needed"

    with open("agent_actions.log", "a") as f:
        f.write(json.dumps(action_log) + "\n")

    return action_log

if __name__ == "__main__":
    logs = read_recent_logs()
    print("=== Recent Logs ===")
    print(logs)

    decision = diagnose(logs)
    print("=== Agent Decision ===")
    print(json.dumps(decision, indent=2))

    result = take_action(decision)
    print("=== Action Taken ===")
    print(json.dumps(result, indent=2))