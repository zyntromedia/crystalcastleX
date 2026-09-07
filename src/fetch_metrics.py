#!/usr/bin/env python3
"""
Fetch GitHub Copilot Organization Metrics
API Docs: https://docs.github.com/rest/copilot/copilot-metrics
"""

import os
import json
import time
import requests
from datetime import datetime

# ─── Configuration ───────────────────────────────────────────────
GITHUB_API_BASE = "https://api.github.com"
API_VERSION = "2022-11-28"  # Required header version

# Get from environment (set in workflow)
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
ORG_NAME = os.getenv("GITHUB_ORG_NAME", "ZyntroAI")  # ← Change your org name!

OUTPUT_DIR = os.path.join(os.path.dirname(__file__), "..", "copilot-metrics")
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ─── Helpers ────────────────────────────────────────────────────
def get_headers():
    return {
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": API_VERSION,
    }

def safe_filename(prefix="copilot-metrics"):
    """Generate filename with UTC timestamp"""
    stamp = datetime.utcnow().strftime("%Y%m%d-%H%M%S-UTC")
    return f"{OUTPUT_DIR}/{prefix}-{stamp}.json"

# ─── Fetch Metrics ──────────────────────────────────────────────
def fetch_copilot_metrics():
    """Fetch Copilot metrics for the organization"""
    url = f"{GITHUB_API_BASE}/orgs/{ORG_NAME}/copilot/metrics"
    print(f"📡 Fetching metrics for org: {ORG_NAME}")

    resp = requests.get(url, headers=get_headers(), timeout=30)

    if resp.status_code == 403:
        print("❌ Permission denied! Check token scopes.")
        print("   Required scopes: manage_billing:copilot OR read:org")
        return None
    if resp.status_code == 404:
        print("❌ Not Found! Verify org name & Copilot Business/Enterprise plan.")
        return None
    if resp.status_code != 200:
        print(f"❌ API Error: HTTP {resp.status_code}")
        print(f"   {resp.text[:500]}")
        return None

    data = resp.json()
    print(f"✅ Retrieved {len(data)} day(s) of metrics")
    return data

# ─── Save Output ────────────────────────────────────────────────
def save_json(data):
    path = safe_filename()
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=2, ensure_ascii=False)
    print(f"💾 Saved → {path}")
    return path

# ─── Summary ─────────────────────────────────────────────────────
def print_summary(data):
    """Print quick summary of latest day's metrics"""
    if not data:
        return
    latest = data[0] if isinstance(data, list) else data
    print("\n📊 Latest Summary:")
    print(f"   Date: {latest.get('date', 'N/A')}")
    print(f"   Active Users: {latest.get('total_active_users', 'N/A')}")
    print(f"   Engaged Users: {latest.get('total_engaged_users', 'N/A')}")

    completions = latest.get("copilot_ide_code_completions", {})
    if completions:
        suggestions = completions.get("total_code_suggestions", 0)
        accepted = completions.get("total_code_acceptances", 0)
        rate = round((accepted / suggestions * 100), 1) if suggestions > 0 else 0
        print(f"   Code Suggestions: {suggestions} | Accepted: {accepted} | Rate: {rate}%")

# ─── Main ────────────────────────────────────────────────────────
if __name__ == "__main__":
    if not GITHUB_TOKEN:
        print("❌ Missing GITHUB_TOKEN environment variable!")
        exit(1)

    metrics = fetch_copilot_metrics()
    if not metrics:
        exit(1)

    save_json(metrics)
    print_summary(metrics)
    print("\n✅ Done!")
