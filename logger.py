import os
import sys
import datetime
from supabase import create_client, Client

def log_event():
    url = os.environ.get("SUPABASE_URL")
    key = os.environ.get("SUPABASE_KEY")
    if not url or not key:
        print("Error: SUPABASE_URL or SUPABASE_KEY not set.")
        sys.exit(1)

    supabase: Client = create_client(url, key)
    
    data = {
        "content": "Wazuh Alert Check (2026-05-04): Connected as clawbot to 208.87.135.185. Blocked by sudo password requirements and directory permissions while trying to read /var/ossec/logs/alerts/alerts.json.",
        "category": "incident_response",
        "importance": 7
    }
    
    try:
        response = supabase.table("agent_memories").insert(data).execute()
        print(f"Logged to Supabase (agent_memories): {response}")
    except Exception as e:
        print(f"Failed to log to Supabase: {e}")

if __name__ == "__main__":
    log_event()
