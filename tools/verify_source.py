#!/usr/bin/env python3
"""Re-download the pinned upstream yellowpaper and check it against SOURCE.json.

The pin is what makes this translation auditable: it names the exact bytes that were
translated, so a reader can diff against them and an upstream revision cannot silently
change what this repository claims to mirror. A mismatch means either the pin is wrong
or the fetch was tampered with — not that upstream moved, because the URL names a commit.
"""
import hashlib, json, sys, urllib.request

meta = json.load(open("SOURCE.json", encoding="utf-8"))["source"]
print(f"{meta['work']} {meta['version']}")
print(f"  commit {meta['commit']}")
print(f"  expect sha256 {meta['sha256']}  ({meta['bytes']:,} bytes)")

req = urllib.request.Request(meta["raw_url"], headers={"User-Agent": "flop-yellowpaper-ko/verify"})
try:
    raw = urllib.request.urlopen(req, timeout=30).read()
except Exception as e:  # noqa: BLE001
    sys.exit(f"  fetch failed: {type(e).__name__}: {e}")

got = hashlib.sha256(raw).hexdigest()
print(f"  got    sha256 {got}  ({len(raw):,} bytes)")
if got == meta["sha256"] and len(raw) == meta["bytes"]:
    print("\nOK — the pinned upstream text is byte-identical to what was translated.")
    sys.exit(0)
sys.exit("\nMISMATCH — do not trust this checkout's provenance claim until it is resolved.")
