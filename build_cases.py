"""Generates the 25 known-difference test pairs in tests/cases/.

Run once:  python build_cases.py
Each case gets a folder with a.txt, b.txt and expected.json.
"""
import json
from pathlib import Path

BASE = (
    "Service Agreement\n\n"
    "1. The Client shall pay the Provider within 30 days of invoice.\n"
    "2. Either party may terminate this agreement with 60 days written notice.\n"
    "3. The Provider will keep all Client data confidential.\n"
    "4. This agreement is governed by the laws of Pakistan.\n"
)

def sub(old, new, text=BASE):
    assert old in text, old
    return text.replace(old, new)

CASES = [
    # --- meaning changes (10) ---
    ("01_payment_days", "meaning_change", BASE, sub("within 30 days", "within 15 days")),
    ("02_negation", "meaning_change", BASE, sub("will keep", "will not keep")),
    ("03_amount", "meaning_change", "The total fee is $5,000 payable in advance.\n", "The total fee is $50,000 payable in advance.\n"),
    ("04_date", "meaning_change", "Delivery is due on 15 March 2026.\n", "Delivery is due on 15 September 2026.\n"),
    ("05_may_to_must", "meaning_change", BASE, sub("may terminate", "must terminate")),
    ("06_liability", "meaning_change", "The Provider is not liable for indirect losses.\n", "The Provider is liable for indirect losses.\n"),
    ("07_shall_to_may", "meaning_change", BASE, sub("shall pay", "may pay")),
    ("08_party_name", "meaning_change", "This contract is between Alpha Traders and Beta Logistics.\n", "This contract is between Alpha Traders and Gamma Logistics.\n"),
    ("09_jurisdiction", "meaning_change", "Disputes will be settled in the courts of Lahore.\n", "Disputes will be settled in the courts of Karachi.\n"),
    ("10_percentage", "meaning_change", "A late fee of 5% applies to overdue invoices.\n", "A late fee of 15% applies to overdue invoices.\n"),
    # --- cosmetic only (6) ---
    ("11_kindly_please", "cosmetic", "Kindly submit the form by Friday.\n", "Please submit the form by Friday.\n"),
    ("12_utilize_use", "cosmetic", "Staff must utilize the approved template.\n", "Staff must use the approved template.\n"),
    ("13_line_breaks", "cosmetic", "The Client pays within 30 days.\nThe Provider keeps data private.\n", "The Client pays within 30 days. The Provider keeps data private.\n"),
    ("14_capitalization", "cosmetic", "the provider will deliver the report.\n", "The Provider will deliver the report.\n"),
    ("15_synonym_buy", "cosmetic", "The company will purchase new laptops.\n", "The company will buy new laptops.\n"),
    ("16_extra_spaces", "cosmetic", "All  invoices  are  payable  monthly.\n", "All invoices are payable monthly.\n"),
    # --- additions (3) ---
    ("17_added_warranty", "addition", BASE, BASE + "5. The Provider warrants all work for 12 months.\n"),
    ("18_added_sentence", "addition", "The Provider will deliver the report.\n", "The Provider will deliver the report. The Client must review it within 7 days.\n"),
    ("19_added_bullet", "addition", "Deliverables:\n- Design\n- Code\n", "Deliverables:\n- Design\n- Code\n- User training\n"),
    # --- removals (3) ---
    ("20_removed_termination", "removal", BASE, sub("2. Either party may terminate this agreement with 60 days written notice.\n", "")),
    ("21_removed_paragraph", "removal", BASE, sub("3. The Provider will keep all Client data confidential.\n", "")),
    ("22_removed_deadline", "removal", "Submit the report. The deadline is 1 December.\n", "Submit the report.\n"),
    # --- identical (2) ---
    ("23_identical", "identical", BASE, BASE),
    ("24_trailing_newline", "identical", BASE, BASE + "\n"),
    # --- mixed: cosmetic + one real change (1) ---
    ("25_mixed", "meaning_change", "Kindly pay within 30 days.\n", "Please pay within 10 days.\n"),
]

def main():
    root = Path(__file__).parent / "tests" / "cases"
    for name, label, a, b in CASES:
        d = root / name
        d.mkdir(parents=True, exist_ok=True)
        (d / "a.txt").write_text(a, encoding="utf-8")
        (d / "b.txt").write_text(b, encoding="utf-8")
        (d / "expected.json").write_text(json.dumps({"label": label}, indent=2), encoding="utf-8")
    print(f"Created {len(CASES)} test cases in {root}")

if __name__ == "__main__":
    main()
