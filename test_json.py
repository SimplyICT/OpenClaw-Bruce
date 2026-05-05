import json
import sys

try:
    with open('/data/.openclaw/openclaw.json', 'r') as f:
        data = json.load(f)
    
    with open('discord_token.txt', 'r') as f:
        token = f.read().strip()

    # Safely inject the plugin structure
    if "plugins" not in data:
        data["plugins"] = {"entries": {}}
    
    data["plugins"]["entries"]["discord-bot"] = {
        "config": {
            "token": token
        },
        "enabled": True
    }

    # Verify JSON serializability
    json.dumps(data)
    print("JSON VALIDATION SUCCESSFUL")
    
    # Create the patch file for user review or application
    with open('openclaw_discord_patch.json', 'w') as f:
        json.dump(data, f, indent=2)

except Exception as e:
    print(f"JSON VALIDATION FAILED: {str(e)}")
    sys.exit(1)
