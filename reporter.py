import os
import sys
from datetime import datetime
from supabase import create_client, Client

def generate_consolidated_report(site_name, target_date):
    url = "https://zhvxjuhgfudavxrfsasn.supabase.co"
    key = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InpodnhqdWhnZnVkYXZ4cmZzYXNuIiwicm9sZSI6InNlcnZpY2Vfcm9sZSIsImlhdCI6MTc3Njc5OTQxOSwiZXhwIjoyMDkyMzc1NDE5fQ.-Y38GK4eJ6ddTRnMKnoCF1iQIdmiwAYEbvuSeKTDd4E"
    supabase = create_client(url, key)
    
    # 1. Pull EVERY device entry for the site
    res = supabase.table('audit_entries').select('*, devices(*)').eq('site_name', site_name).order('audit_date', desc=True).execute()
    raw_data = res.data

    if not raw_data:
        print(f"No records found.")
        return

    # 2. Deduplicate: keep only the most recent audit per serial number
    unique_devices = {}
    for entry in raw_data:
        sn = entry['serial_number']
        if sn and sn not in unique_devices:
            unique_devices[sn] = entry
    
    data = list(unique_devices.values())
    
    # 3. Categorize for parts of the report
    active_devices = [r for r in data if not r.get('ignore_flag')]
    missing_assets = [r for r in data if r.get('ignore_flag')]
    photo_breaches = [r for r in data if r.get('photos_count', 0) > 100]
    
    report = []
    report.append(f"# Site Audit Report: {site_name}")
    report.append(f"Comprehensive Fleet Summary - Generated {datetime.now().strftime('%d %B %Y')}")
    
    # --- Executive Summary ---
    report.append("\n## EXECUTIVE SUMMARY")
    report.append(f"• **Asset Coverage:** {len(data)} total devices identified.")
    report.append(f"• **Active Inventory:** {len(active_devices)} devices confirmed operational.")
    report.append(f"• **Flagged Assets:** {len(missing_assets)} devices currently marked missing / ignore.")
    if photo_breaches:
        report.append(f"• **Compliance Alerts:** {len(photo_breaches)} devices exceed local photo storage limits.")

    # --- Critical Incidents & Immediate Actions ---
    report.append("\n## CRITICAL INCIDENTS & IMMEDIATE ACTIONS")
    found_critical = False
    if missing_assets:
        found_critical = True
        report.append("### Assets Requiring Immediate Investigation")
        for m in missing_assets:
            dev = m.get('devices') or {}
            report.append(f"- **MISSING:** Room: {dev.get('assigned_user_room', 'N/A')} | SN: {m['serial_number']} | Model: {dev.get('brand_model', 'N/A')}")
    
    if photo_breaches:
        found_critical = True
        report.append("### Photo Retention Breaches")
        for p in photo_breaches:
            dev = p.get('devices') or {}
            report.append(f"- **PRIVACY:** Room: {dev.get('assigned_user_room', 'N/A')} | SN: {p['serial_number']} | Count: {p['photos_count']} Photos")
            
    if not found_critical:
        report.append("• No critical security incidents or immediate compliance actions required at this time.")

    # --- Detailed Audit Findings ---
    report.append("\n## DETAILED AUDIT FINDINGS BY ROOM / USER")
    data.sort(key=lambda x: (str((x.get('devices') or {}).get('assigned_user_room') or '').lower()))
    
    for r in data:
        dev = r.get('devices') or {}
        report.append(f"\n### Room: {dev.get('assigned_user_room', 'Unassigned')}")
        report.append(f"**Asset:** {dev.get('brand_model', 'Unknown')} | **SN:** {r['serial_number']}")
        
        dtype = (dev.get('device_type') or "").lower()
        if "tablet" in dtype or "phone" in dtype:
            report.append(f"- **OS Version:** iOS {r.get('ios_version') or 'N/A'}")
            report.append(f"- **Cloud Sync:** Camera: {'OFF (Pass)' if r.get('camera_sync_off') else 'ON (Check)'} | OneDrive: {'ON (Pass)' if r.get('onedrive_sync_on') else 'OFF (Action required)'}")
            report.append(f"- **Photos:** {r.get('photos_count', 0)} files recorded on {r.get('photos_date') or 'N/A'}")
        else:
            report.append(f"- **OS Version:** Windows {r.get('windows_os') or 'N/A'}")
            report.append(f"- **Compliance:** Updates: {r.get('update_status') or 'N/A'} | Security Check: {r.get('security_check') or 'N/A'}")

        if r.get('notes'):
            report.append(f"- **Engineer Notes:** {r['notes']}")

    # --- Missing Assets Register ---
    if missing_assets:
        report.append("\n## MISSING ASSETS REGISTER")
        for m in missing_assets:
            dev = m.get('devices') or {}
            report.append(f"• **{m['serial_number']}** ({dev.get('brand_model', 'Unknown')}) - Last known in Room: {dev.get('assigned_user_room', 'N/A')}")

    final_report = "\n".join(report)
    fn = f"report_{site_name.replace(' ', '_')}_{target_date}.md"
    with open(fn, 'w') as f: f.write(final_report)
    print(f"Success: Consolidated report with all sections generated.")

if __name__ == "__main__":
    if len(sys.argv) > 2: generate_consolidated_report(sys.argv[1], sys.argv[2])
