#!/bin/bash
# Bruce recovery script for Railway/Docker
# Usage: bash recovery.sh <GITHUB_PAT>

GITHUB_REPO="https://DavidCartledge:$1@github.com/SimplyICT/OpenClaw-Bruce.git"
DEST="/data/workspace"

echo "🛡️ Bruce Recovery Started..."

if [ -z "$1" ]; then
    echo "❌ Error: Missing GitHub PAT. Usage: bash recovery.sh <PAT>"
    exit 1
fi

# 1. Sync from GitHub
echo "📂 Syncing workspace from GitHub..."
git clone $GITHUB_REPO temp_recovery
cp -rv temp_recovery/* $DEST/
cp -rv temp_recovery/.openclaw $DEST/
rm -rf temp_recovery

# 2. Restore global OpenClaw configuration
echo "⚙️ Restoring OpenClaw configuration..."
mkdir -p /data/.openclaw
cp -v $DEST/.openclaw/openclaw.json /data/.openclaw/openclaw.json

# 3. Setup Supabase Memory Skill (Re-installing dependencies)
echo "🧠 Re-initializing Supabase Memory..."
bash /data/.openclaw/skills/supabase-memory/scripts/setup.sh

# 4. Restart Gateway note
echo "✅ Recovery complete. Please RESTART the Railway service to load the new config."
