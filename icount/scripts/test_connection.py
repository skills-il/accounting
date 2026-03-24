#!/usr/bin/env python3
"""
Verify that your ICOUNT_API_KEY is valid and working.
Run: python scripts/test_connection.py

Requires: pip install requests
Set ICOUNT_API_KEY in your environment or .env file.
"""

import os
import sys

try:
    import requests
except ImportError:
    print("Missing dependency: pip install requests")
    sys.exit(1)

# Load .env if present
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.getenv("ICOUNT_API_KEY")
if not API_KEY:
    print("ERROR: ICOUNT_API_KEY not set.")
    print("Set it in your .env file or environment: export ICOUNT_API_KEY=your_key")
    sys.exit(1)

BASE_URL = "https://api.icount.co.il/api/v3.php"

def icount_post(endpoint, data=None):
    resp = requests.post(
        f"{BASE_URL}/{endpoint}",
        headers={"Authorization": f"Bearer {API_KEY}"},
        data=data or {},
    )
    return resp.json()

print("Testing iCount API connection...")
print(f"Key: {API_KEY[:8]}...")

# Test 1: list clients (lightweight call)
result = icount_post("client/get_list")
if not result.get("status"):
    reason = result.get("reason", "unknown")
    desc = result.get("error_description", "")
    print(f"\nFAILED: [{reason}] {desc}")
    if reason == "auth_required":
        print("Your API key is invalid or expired. Check iCount under Settings → API.")
    sys.exit(1)

count = result.get("clients_count", "?")
print(f"\nSUCCESS — connected to iCount.")
print(f"Clients in account: {count}")

# Test 2: get doc types
result2 = icount_post("doc/types")
if result2.get("status") and result2.get("types"):
    types = result2["types"]
    print(f"Document types available: {len(types)}")
    for t in types[:5]:
        print(f"  - {t.get('doctype')}: {t.get('name_he', t.get('name', ''))}")
    if len(types) > 5:
        print(f"  ... and {len(types) - 5} more (run list_doctypes.py for full list)")

print("\nAll checks passed. You're ready to use the iCount API.")
