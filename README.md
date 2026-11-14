# Scheme Saathi

A simple bilingual (English/Hindi) government-scheme eligibility and guidance chatbot.

## Run locally
1. Install Python 3.10 or newer.
2. Open a terminal in this folder.
3. Run: `pip install -r requirements.txt`
4. Set your Gemini API key as an environment variable named `GEMINI_API_KEY`.
5. Run: `streamlit run app.py`

## Add verified schemes
Edit `schemes.json`. Add only information checked against an official government source.
Each record should follow this structure:

```json
{
  "name": "Official scheme name",
  "description": "Short description from the official source",
  "eligibility": {
    "age_min": null,
    "age_max": null,
    "max_annual_family_income_inr": null,
    "states": [],
    "occupations": [],
    "categories": []
  },
  "required_documents": [],
  "application_steps": [],
  "source_url": "https://official-government-domain.gov.in/..."
}
```

Use `null` or an empty list when the official source does not specify a condition. Do not guess.
The app uses Gemini to explain only the records supplied in `schemes.json`. It is a guidance tool, not an official eligibility decision.
