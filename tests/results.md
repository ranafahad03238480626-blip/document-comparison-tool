# Test results

Cases: 25
- difflib baseline: 17/25
- AI semantic check (gemini-flash-lite-latest): 24/25

| Case | Expected | Baseline | AI |
|---|---|---|---|
| 01_payment_days | meaning_change | meaning_change | meaning_change |
| 02_negation | meaning_change | addition | meaning_change |
| 03_amount | meaning_change | meaning_change | meaning_change |
| 04_date | meaning_change | meaning_change | meaning_change |
| 05_may_to_must | meaning_change | meaning_change | cosmetic |
| 06_liability | meaning_change | removal | meaning_change |
| 07_shall_to_may | meaning_change | meaning_change | meaning_change |
| 08_party_name | meaning_change | meaning_change | meaning_change |
| 09_jurisdiction | meaning_change | meaning_change | meaning_change |
| 10_percentage | meaning_change | meaning_change | meaning_change |
| 11_kindly_please | cosmetic | meaning_change | cosmetic |
| 12_utilize_use | cosmetic | meaning_change | cosmetic |
| 13_line_breaks | cosmetic | identical | cosmetic |
| 14_capitalization | cosmetic | meaning_change | cosmetic |
| 15_synonym_buy | cosmetic | meaning_change | cosmetic |
| 16_extra_spaces | cosmetic | identical | cosmetic |
| 17_added_warranty | addition | addition | addition |
| 18_added_sentence | addition | addition | addition |
| 19_added_bullet | addition | addition | addition |
| 20_removed_termination | removal | removal | removal |
| 21_removed_paragraph | removal | removal | removal |
| 22_removed_deadline | removal | removal | removal |
| 23_identical | identical | identical | identical |
| 24_trailing_newline | identical | identical | identical |
| 25_mixed | meaning_change | meaning_change | meaning_change |