#!/usr/bin/env python3
"""Check that verbatim classes survived translation, section by section.

A reader of a translated specification cannot see a dropped requirement ID or a mutated
figure, but an implementer would act on it. So the classes that must never change —
identifiers, parameter names, numbers, RFC 2119 keywords, anchors — are counted in the
pinned English source and in the Korean, per section. Extra occurrences are fine: Korean
word order often repeats an ID. Missing ones are defects.

Self-contained: it fetches the pinned source named by SOURCE.json (cached under .cache/),
splits it on "## " the same way the translation was split, and compares.

    python3 tools/check_fidelity.py            # compare, exit 1 on any discrepancy
    python3 tools/check_fidelity.py --verbose  # also print per-class totals per section

KNOWN EXCEPTION (reported, intentional): Appendix A's "parts-per-10,000" is rendered
"1만분율". It is a unit expression, not a figure, so translating it is correct.
"""
from __future__ import annotations

import argparse
import collections
import hashlib
import json
import os
import re
import sys
import urllib.request

ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
KO = os.path.join(ROOT, "ko")
CACHE = os.path.join(ROOT, ".cache")

# Python's \b treats Hangul as a word character, so "E.46이" — an identifier with a Korean
# particle glued to it — does not end on a boundary and vanishes from the counts. The first
# run of this check reported 47 phantom defects for exactly that reason. Bound each class on
# ASCII continuation only: a token is clipped only if MORE OF ITS OWN alphabet follows.
NOT_ID = r"(?![0-9A-Za-z_.-])"
# A Korean sentence may put a comma straight after a figure ("3,500,000,000, 네 코호트"),
# so only a digit continuation means the number was cut short.
NOT_NUM = r"(?![0-9])(?![,_]\d)"

CLASSES = {
    "requirement id": re.compile(r"\bR\d+\.\d+[a-z]?" + NOT_ID),
    "decision id":    re.compile(r"\bD-\d{4}" + NOT_ID),
    "open item":      re.compile(r"\bE\.\d+" + NOT_ID),
    "invariant":      re.compile(r"\bINV-\d+" + NOT_ID),
    "spec id":        re.compile(r"\b(?:SPEC|ECON|GOV|ENG)-[0-9A-Za-z]+" + NOT_ID),
    "param name":     re.compile(r"`([a-z][a-z0-9_]{4,})`"),
    "big number":     re.compile(r"\b\d{1,3}(?:[,_]\d{3})+" + NOT_NUM),
    "rfc2119":        re.compile(r"\*\*(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY)\*\*"),
    "anchor":         re.compile(r'id="([^"]+)"'),
}

# Section index -> translated filename, in the order the source presents them.
KNOWN_EXCEPTIONS = {("17-Appendix-A-Parameter-Reference.md", "big number", "10,000")}


def pinned_source() -> str:
    meta = json.load(open(os.path.join(ROOT, "SOURCE.json"), encoding="utf-8"))["source"]
    os.makedirs(CACHE, exist_ok=True)
    path = os.path.join(CACHE, f"{meta['commit'][:12]}-{meta['file']}")
    if not os.path.exists(path):
        req = urllib.request.Request(meta["raw_url"],
                                     headers={"User-Agent": "flop-yellowpaper-ko/fidelity"})
        raw = urllib.request.urlopen(req, timeout=30).read()
        if hashlib.sha256(raw).hexdigest() != meta["sha256"]:
            sys.exit("pinned source hash mismatch — run tools/verify_source.py")
        open(path, "wb").write(raw)
    raw = open(path, "rb").read()
    if hashlib.sha256(raw).hexdigest() != meta["sha256"]:
        sys.exit(f"cached copy corrupted; delete {path}")
    return raw.decode()


def split_sections(text: str) -> list[tuple[str, str]]:
    """(front matter, then one entry per '## ' section) — the split the translation used."""
    i = text.find("\n## ")
    out = [("00-front.md", text[:i])]
    for part in re.split(r"\n(?=## )", text[i:]):
        if part.strip():
            out.append((None, part))
    return out


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__,
                                 formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--verbose", action="store_true")
    args = ap.parse_args()

    ko_files = sorted(f for f in os.listdir(KO) if f.endswith(".md"))
    sections = split_sections(pinned_source())
    if len(sections) != len(ko_files):
        return int(bool(print(f"section count differs: source {len(sections)}, "
                              f"translation {len(ko_files)}")))

    totals = collections.Counter()
    problems, excused = [], []
    for (_, src_text), fn in zip(sections, ko_files):
        ko_text = open(os.path.join(KO, fn), encoding="utf-8").read()
        for name, rx in CLASSES.items():
            ca = collections.Counter(rx.findall(src_text))
            cb = collections.Counter(rx.findall(ko_text))
            for tok, n in ca.items():
                totals[name] += n
                if cb.get(tok, 0) < n:
                    row = (fn, name, tok, n, cb.get(tok, 0))
                    (excused if (fn, name, tok) in KNOWN_EXCEPTIONS else problems).append(row)
        if args.verbose:
            print(f"{fn[:50]:52} " + " ".join(
                f"{k[:4]}={len(set(rx.findall(src_text)))}" for k, rx in CLASSES.items()))

    print(f"sections compared: {len(ko_files)}")
    print("verbatim tokens checked:", dict(totals))
    for fn, cls, tok, n, m in excused:
        print(f"\nknown exception: {fn} [{cls}] {tok!r} source {n}, translation {m}"
              f"\n  rendered into Korean on purpose; see the note in this file's docstring.")
    if not problems:
        print("\nPASS — every identifier, parameter name, figure, RFC 2119 keyword and "
              "anchor in the pinned source survives in the translation.")
        return 0
    print(f"\nFAIL — {len(problems)} discrepancies:")
    for fn, cls, tok, n, m in problems[:80]:
        print(f"  {fn[:46]:48} [{cls}] {tok!r}: source {n}, translation {m}")
    if len(problems) > 80:
        print(f"  … {len(problems) - 80} more")
    return 1


if __name__ == "__main__":
    sys.exit(main())
