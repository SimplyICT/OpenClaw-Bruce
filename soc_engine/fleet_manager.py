import sys
import subprocess
import json
import time

# --- ASGARDIAN FLEET CONFIGURATION MANAGER ---
# Goal: Programmatically update agent visibility across the 29+ nodes.

WAZUH_SERVER = "clawbot@208.87.135.185"

def push_huntress_policy():
    """
    Erik Selvig's Directive: Push a unified FIM policy to all agents 
    to monitor classic persistence footholds (Tasks, RunKeys).
    """
    # Define the professional Huntress-style monitoring block
    windows_policy = """
    <syscheck>
      <directories check_all="yes" realtime="yes">C:\\Windows\\System32\\Tasks</directories>
      <windows_registry arch="both" check_all="yes" realtime="yes">HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\Run</windows_registry>
      <windows_registry arch="both" check_all="yes" realtime="yes">HKEY_LOCAL_MACHINE\\Software\\Microsoft\\Windows\\CurrentVersion\\RunOnce</windows_registry>
    </syscheck>
    """
    
    print("🛰️ Asgard Fleet Manager: Deploying Huntress-mimic policy to shared configuration...")
    
    # In a professional Wazuh environment, we use 'agent.conf' in the shared groups.
    # For now, we apply to the default group to ensure immediate total-fleet visibility.
    cmd = f"echo '{windows_policy}' | sudo -n tee /var/ossec/etc/shared/default/agent.conf > /dev/null"
    
    try:
        subprocess.check_call(["ssh", WAZUH_SERVER, cmd])
        print("✅ Policy Staged. Blasting restart signal to 29+ agents...")
        subprocess.check_call(["ssh", WAZUH_SERVER, "sudo -n /var/ossec/bin/agent_control -R -a"])
        return True
    except Exception as e:
        print(f"❌ Fleet Deployment Failed: {e}")
        return False

if __name__ == "__main__":
    push_huntress_policy()
