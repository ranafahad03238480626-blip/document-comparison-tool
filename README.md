# AI Document Comparison Tool

A Streamlit app that takes two versions of a document and explains **what changed in meaning**, not just in wording.

Upload two files (PDF, DOCX or TXT), click **Compare Documents**, and get:

- a text similarity score
- the content that was added and removed
- the full line-by-line difference
- an AI semantic analysis of which changes actually alter the meaning
- a downloadable report (`.txt`)

**Live app:** https://document-comparison-tool-tqttsqccb7wgtd4354fgms.streamlit.app/

## How it works

1. Text is extracted from each uploaded file (PDF, DOCX or TXT).
2. A text diff finds added, removed and changed content and a similarity score.
3. The changes are sent to an LLM, which explains which ones change the meaning
   (numbers, dates, names, obligations, negations) and which are only rewording.
4. Everything is combined into a report the user can download.

## Tech

- Python, Streamlit
- PDF/DOCX/TXT text extraction
- `difflib` for the text diff
- An OpenAI-compatible chat API for the semantic analysis. The app runs with
  OpenAI or with Google Gemini through its OpenAI-compatible endpoint
  (set `OPENAI_BASE_URL` and `OPENAI_MODEL`).

## Setup

```bash
git clone <your-repo-url>
cd Document_Comparison_Tool
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

Create a `.env` file (never commit it) based on `.env.example`:

```
OPENAI_API_KEY=your_key_here
# Optional, only when using Gemini:
# OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
# OPENAI_MODEL=gemini-flash-latest
```

Run:

```bash
streamlit run app.py
```

## Testing

The repo ships with 25 test pairs with known differences in `tests/cases/`:
10 meaning changes (numbers, dates, negation, names, obligations), 6 cosmetic
rewordings, 3 additions, 3 removals, 2 identical files and 1 mixed case.

```bash
python build_cases.py   # (re)generate the cases
python run_tests.py     # needs the API key in .env
python run_tests.py --offline   # difflib baseline only
```

Results (evaluation run with `gemini-flash-lite-latest`; full expected vs actual table for all 25 cases: [tests/results.md](tests/results.md)):

| Method | Correct |
|---|---|
| Plain text diff (difflib) only | 17 / 25 |
| Text diff + AI semantic check | 24 / 25 |

A plain diff cannot tell rewording ("Kindly" -> "Please") from a real change
("will" -> "will not"), so it labels every difference as a change. The AI check
fixes this. Per-case results are written to `tests/results.md`.

The one case the AI check got wrong is `05_may_to_must` ("may terminate" -> "must terminate"): it was labelled cosmetic, but the change from permission to obligation is a meaning change.

## Known limitations

- The AI step needs an API key and can be slow or rate-limited on free tiers.
- Scanned PDFs (images without text) are not supported, there is no OCR.
- Very long documents may need to be split before they are sent to the model.
- AI output can occasionally be wrong, so important changes should be reviewed by a human.

## Security

API keys are read from environment variables. `.env` is in `.gitignore`;
only `.env.example` (with a placeholder) is committed.
