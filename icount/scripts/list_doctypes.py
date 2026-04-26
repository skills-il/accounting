#!/usr/bin/env python3
"""
List all document types available in your iCount account.
Run: python scripts/list_doctypes.py

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

try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

API_KEY = os.getenv("ICOUNT_API_KEY")
if not API_KEY:
    print("ERROR: ICOUNT_API_KEY not set.")
    sys.exit(1)

resp = requests.post(
    "https://api.icount.co.il/api/v3.php/doc/types",
    headers={"Authorization": f"Bearer {API_KEY}"},
    data={},
)
result = resp.json()

if not result.get("status"):
    print(f"ERROR: {result.get('reason')} — {result.get('error_description', '')}")
    sys.exit(1)

types = result.get("types", [])
print(f"Document types for your account ({len(types)} total):\n")
print(f"{'doctype':<12} {'Hebrew name':<30} {'English name'}")
print("-" * 60)
for t in types:
    doctype = t.get("doctype", "")
    name_he = t.get("name_he") or t.get("name", "")
    name_en = t.get("name_en") or ""
    print(f"{doctype:<12} {name_he:<30} {name_en}")
