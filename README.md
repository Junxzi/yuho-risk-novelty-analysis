## Reproducibility Repository (Japan Stocks: Novelty of Risk Disclosures × Market Reaction)

This repository bundles the empirical pipeline used in my undergraduate thesis in a way that allows **third parties to reproduce the results**.

- EDINET annual securities reports → extract the “Business Risks” section
- Build **novelty / change** measures based on embeddings (sentence-transformers) + cosine similarity
- Event study using the filing date as the event date (abnormal volume, CAR, \(\sum |AR|\), etc.)
- Regression analysis and robustness checks (pre-trends, placebo event dates, etc.)

### Included / Not included
- **Included**: notebooks, scripts, DB schema (`sql/`), dependencies (`requirements.txt`).
- **Not included**: raw data or large intermediate artifacts (see `.gitignore`).  
  Due to data licensing/usage constraints and file sizes, **`data/` and `outputs/` are not included**.

## Quickstart (DB + Python)

### Verified Python version
- **Python 3.10.18** (the environment used when creating the notebooks; using Python 3.10.x is recommended for reproduction)

### 1) Create `.env`
Create `.env` at the repository root (template: `config/env.example`).

```bash
cp config/env.example .env
```

### 2) Start PostgreSQL
Start your PostgreSQL instance (e.g., via Docker Compose or your local setup).

> On first run, tables are created using `sql/001_schema.sql`.

### 3) Install Python dependencies
```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 4) Run notebooks (recommended order)
- `notebooks/02_fetch_yuho.ipynb`: Register EDINET document metadata (`edinet_documents`)
- `notebooks/03_extract_risk_section.ipynb`: Extract the “Business Risks” section (saved locally)
- `notebooks/04_upsert_risk_section.ipynb`: Upsert extracted text into DB (`risk_text`)
- `notebooks/06_fetch_control_variable_elements.ipynb`: Extract/register control variables (financial items)
- `notebooks/08_calculate_similarity.ipynb`: Compute similarity / novelty (pairwise)
- `notebooks/09_chunk_change_scores.ipynb`: Build aggregated measures (e.g., `change_topk`)
- `notebooks/10_event_study_market_model.ipynb` / `notebooks/11_event_study_uncertainty.ipynb`: Compute event-window outcomes
- `notebooks/14_results_writeup.ipynb`: Generate final results (tables/figures)

### Notes on credentials and data acquisition
- EDINET-derived data, as well as stock price and financial statement data, must be prepared separately in accordance with each data provider’s terms of use.
- If you use J-Quants, set `JPX_API_KEY` / `JQUANTS_USER` / `JQUANTS_PASS` in `.env` (only required for relevant notebooks).
