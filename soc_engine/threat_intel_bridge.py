import os
import json
import requests
import time
from supabase import create_client

# --- ASGARDIAN THREAT INTEL BRIDGE ---
VT_API_KEY = "50b81d2d1082922953a9ad5aa13c4de5afde6bd6ca6b738a0e933364b6142367"
SUPABASE_URL = "https://zhvxjuhgfudavxrfsasn.supabase.co"
SUPABASE_KEY = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"

def check_file_hash(file_hash):
    """Mimic Huntress analysis by checking a hash against VirusTotal."""
    url = f"https://www.virustotal.com/api/v3/files/{file_hash}"
    headers = {"x-apikey": VT_API_KEY}
    try:
        res = requests.get(url, headers=headers, timeout=10)
        if res.status_code == 200:
            stats = res.json()['data']['attributes']['last_analysis_stats']
            malicious = stats.get('malicious', 0)
            return {"status": "SUCCESS", "malicious_count": malicious, "stats": stats}
        return {"status": "NOT_FOUND", "message": "Hash not in VT database."}
    except Exception as e:
        return {"status": "ERROR", "message": str(e)}

def log_intel_to_squad(agent, target, result):
    sb = create_client(SUPABASE_URL, SUPABASE_KEY)
    malicious = result.get('malicious_count', 0)
    
    summary = f"INTEL SCAN: {target}"
    intel = f"VT_SCORE: {malicious} engines flagged this || HASH: {target}"
    remediation = "ACTION: Confirming persistent foothold status. Awaiting deeper behavioral scan." if malicious > 0 else "ACTION: No immediate threat found in global database."

    data = {
        "agent_name": agent,
        "task_description": f"{summary} || {intel} || {remediation}",
        "status": "RESPONDING" if malicious > 2 else "ACTIVE",
        "model_used": "Asgard-Intel-Bridge-v1"
    }
    sb.table("agent_logs").insert(data).execute()

if __name__ == "__main__":
    # Test run for internal verification
    print("🦞 Asgard Threat Intel Bridge: Testing VT link...")
    # Example: EICAR hash
    test_hash = "275a021bbfb6489e54d471899f7db9d1663fc695ec2fe2a2c4538aabf651fd0f"
    result = check_file_hash(test_hash)
    print(f"Test Result: {result}")
    log_intel_to_squad("Heimdall", "EICAR_TEST_HASH", result)
