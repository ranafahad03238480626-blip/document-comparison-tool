"""Runs all test cases in tests/cases/ and prints an accuracy score.

Usage:
  python run_tests.py            # difflib baseline + AI semantic check (needs OPENAI_API_KEY)
  python run_tests.py --offline  # difflib baseline only (no API key needed)

Labels: identical | cosmetic | meaning_change | addition | removal
Results are written to tests/results.md
"""
import argparse
import difflib
import json
import os
import re
import sys
import time
from pathlib import Path

try:
    from dotenv import load_dotenv
    load_dotenv(override=True)
except ImportError:
    pass

CASES_DIR = Path(__file__).parent / "tests" / "cases"
MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
LABELS = ["identical", "cosmetic", "meaning_change", "addition", "removal"]

PROMPT = """You compare two versions of a document (A = old, B = new).
Decide what kind of change happened. Answer with JSON only:
{"label": "<one of identical|cosmetic|meaning_change|addition|removal>", "summary": "<one sentence>"}

Definitions:
- identical: same content (only trailing whitespace may differ)
- cosmetic: wording, spelling, capitalization, spacing or formatting changed but the MEANING is the same
- meaning_change: a fact, number, date, name, obligation, negation or condition changed
- addition: new content was added and nothing else changed meaning
- removal: content was deleted and nothing else changed meaning
If several apply, pick the most significant one (meaning_change wins)."""


def normalize(t: str) -> str:
    return re.sub(r"\s+", " ", t).strip()


def baseline(a: str, b: str) -> str:
    """Word-level diff only: cannot tell cosmetic from meaning changes."""
    if normalize(a) == normalize(b):
        return "identical"
    sm = difflib.SequenceMatcher(None, normalize(a).split(), normalize(b).split())
    ops = {tag for tag, *_ in sm.get_opcodes() if tag != "equal"}
    if ops == {"insert"}:
        return "addition"
    if ops == {"delete"}:
        return "removal"
    return "meaning_change"


def ai_check(client, a: str, b: str) -> str:
    """Calls the model. Retries on rate limit (429) or overload (503)."""
    for attempt in range(6):
        try:
            resp = client.chat.completions.create(
                model=MODEL,
                temperature=0,
                response_format={"type": "json_object"},
                messages=[
                    {"role": "system", "content": PROMPT},
                    {"role": "user", "content": f"A:\n{a}\n\nB:\n{b}"},
                ],
            )
            label = json.loads(resp.choices[0].message.content).get("label", "")
            return label if label in LABELS else "invalid"
        except Exception as e:
            code = getattr(e, "status_code", None)
            if code in (429, 500, 503) and attempt < 5:
                wait = 15 * (attempt + 1)
                print(f"   (error {code}, waiting {wait}s then retrying...)")
                time.sleep(wait)
                continue
            raise
    return "invalid"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--offline", action="store_true")
    args = ap.parse_args()

    client = None
    if not args.offline:
        if not os.getenv("OPENAI_API_KEY"):
            sys.exit("OPENAI_API_KEY not set. Put it in .env or use --offline.")
        from openai import OpenAI
        client = OpenAI()

    cases = sorted(p for p in CASES_DIR.iterdir() if p.is_dir())
    if not cases:
        sys.exit("No cases found. Run: python build_cases.py")

    cache_file = Path(__file__).parent / "tests" / "ai_cache.json"
    cache = json.loads(cache_file.read_text()) if cache_file.exists() else {}

    rows, base_ok, ai_ok = [], 0, 0
    for c in cases:
        a = (c / "a.txt").read_text(encoding="utf-8")
        b = (c / "b.txt").read_text(encoding="utf-8")
        expected = json.loads((c / "expected.json").read_text())["label"]
        base = baseline(a, b)
        if client:
            key = c.name + "|" + MODEL
            if key not in cache:
                cache[key] = ai_check(client, a, b)
                cache_file.write_text(json.dumps(cache, indent=2))
                time.sleep(6)  # stay under the free-tier rate limit
            ai = cache[key]
        else:
            ai = "-"
        base_ok += base == expected
        ai_ok += ai == expected
        rows.append((c.name, expected, base, ai))
        print(f"{c.name:28} expected={expected:15} baseline={base:15} ai={ai}")

    n = len(rows)
    print(f"\nBaseline (difflib only): {base_ok}/{n}")
    if client:
        print(f"AI semantic check:      {ai_ok}/{n}")

    out = ["# Test results", "", f"Cases: {n}", f"- difflib baseline: {base_ok}/{n}"]
    if client:
        out.append(f"- AI semantic check ({MODEL}): {ai_ok}/{n}")
    out += ["", "| Case | Expected | Baseline | AI |", "|---|---|---|---|"]
    out += [f"| {r[0]} | {r[1]} | {r[2]} | {r[3]} |" for r in rows]
    (Path(__file__).parent / "tests" / "results.md").write_text("\n".join(out), encoding="utf-8")


if __name__ == "__main__":
    main()
