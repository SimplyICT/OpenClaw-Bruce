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
        "content": "Initiated project for Offline Audit Database and Web UI. Fields defined include device specs, security settings, and photo analytics. Erik Selvig (sub-agent) tasked with schema design.",
        "category": "project_initialization",
        "importance": 5
    }
    
    try:
        response = supabase.table("agent_memories").insert(data).execute()
        print(f"Logged to Supabase (agent_memories): {response}")
    except Exception as e:
        print(f"Failed to log to Supabase: {e}")

if __name__ == "__main__":
    log_event()
