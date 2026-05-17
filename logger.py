import os
import json
import requests

def log_task(agent_name, task_description, model_used, status):
    # Load Supabase configuration from environment variables (fallback to defaults)
    url = os.getenv("SUPABASE_URL", "https://zhvxjuhgfudavxrfsasn.supabase.co")
    key = os.getenv("SUPABASE_KEY", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E")
    # Supabase REST endpoint for inserting into the "agent_logs" table
    endpoint = f"{url}/rest/v1/agent_logs"
    headers = {
        "apikey": key,
        "Authorization": f"Bearer {key}",
        "Content-Type": "application/json",
        "Prefer": "return=representation"
    }
    data = {
        "agent_name": agent_name,
        "task_description": task_description,
        "model_used": model_used,
        "status": status
    }
    try:
        response = requests.post(endpoint, headers=headers, data=json.dumps(data))
        response.raise_for_status()
        return True
    except Exception as e:
        print(f"Logging failed: {e}")
        return False

if __name__ == "__main__":
    import sys
    if len(sys.argv) == 5:
        success = log_task(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4])
        print("Logged" if success else "Failed")

