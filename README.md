## Reproducibility repository (risk novelty × stock market reaction, Japan)

This repository contains code and notebooks for reproducing the empirical pipeline used in the thesis:

- EDINET annual securities reports (有価証券報告書) → extract “事業等のリスク”
- Construct a **novelty / change** measure using sentence embeddings + cosine similarity
- Event-study style outcomes (abnormal volume, CAR, \(\sum \lvert AR \rvert\))
- Regression analyses and robustness checks (pre-trend, placebo shifted event dates)

### What is included / not included
- **Included**: notebooks, scripts, DB schema (`sql/`), LaTeX thesis sources (`thesis/`), dependency list (`requirements.txt`).
- **Not included**: raw EDINET documents / vendor datasets / large intermediate artifacts (see `.gitignore`).  
  Due to data licensing and size constraints, **`data/` and `outputs/` are intentionally excluded**.

### Quickstart (DB + Python)

1) **Create a `.env`**

Copy `config/env.example` to `.env` at the repository root and fill values:

```bash
cp config/env.example .env
```

2) **Start PostgreSQL**

```bash
docker compose up -d
```

This will create tables using `sql/001_schema.sql` on first initialization.

3) **Install Python dependencies**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

4) **Run notebooks (typical order)**

- `notebooks/02_fetch_yuho.ipynb` (register EDINET docs metadata)
- `notebooks/03_extract_risk_section.ipynb` (extract risk section → `data/processed/...`)
- `notebooks/04_upsert_risk_section.ipynb` (upsert risk_text to DB)
- `notebooks/06_fetch_control_variable_elements.ipynb` (control variables)
- `notebooks/08_calculate_similarity.ipynb` (novelty pairs)
- `notebooks/09_chunk_change_scores.ipynb` (main novelty metric `change_topk`)
- `notebooks/10_event_study_market_model.ipynb` / `11_event_study_uncertainty.ipynb`
- `notebooks/14_results_writeup.ipynb` (final tables/figures used in write-up)

### Notes on credentials & data
- EDINET source data and some market/financial datasets may require separate acquisition.
- If you use J-Quants, set `JPX_API_KEY` / `JQUANTS_USER` / `JQUANTS_PASS` in `.env`.

