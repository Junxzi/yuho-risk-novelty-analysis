-- Minimal schema for reproducing the analysis (no raw data included).
-- This file is mounted into the Postgres container via docker-compose and
-- executed automatically on first initialization.

-- Companies master
CREATE TABLE IF NOT EXISTS companies (
  company_id   UUID PRIMARY KEY,
  corp_number  VARCHAR(13),
  edinet_code  VARCHAR(6),
  security_code VARCHAR(5),
  created_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  updated_at   TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- EDINET document metadata (annual securities reports etc.)
CREATE TABLE IF NOT EXISTS edinet_documents (
  doc_id        VARCHAR(20) PRIMARY KEY,
  company_id    UUID,
  edinet_code   VARCHAR(6),
  doc_type_code VARCHAR(10),
  submit_date   TIMESTAMP,
  fiscal_year   INTEGER,
  description   TEXT,
  local_csv_path TEXT,
  risk_text     TEXT,
  risk_count    INTEGER
);

CREATE INDEX IF NOT EXISTS idx_edinet_documents_company_year
  ON edinet_documents(company_id, fiscal_year);

-- Daily quotes (J-Quants downloader notebook creates/uses this)
CREATE TABLE IF NOT EXISTS daily_quotes (
  code              VARCHAR(5)  NOT NULL,
  date              DATE        NOT NULL,
  open              NUMERIC(10,2),
  high              NUMERIC(10,2),
  low               NUMERIC(10,2),
  close             NUMERIC(10,2),
  volume            BIGINT,
  turnover_value    BIGINT,
  adjustment_factor NUMERIC(9,6),
  adjusted_open     NUMERIC(10,2),
  adjusted_high     NUMERIC(10,2),
  adjusted_low      NUMERIC(10,2),
  adjusted_close    NUMERIC(10,2),
  adjusted_volume   BIGINT,
  upper_limit       BOOLEAN,
  lower_limit       BOOLEAN,
  PRIMARY KEY (code, date)
);

-- Control variables extracted from EDINET CSV (balance sheet / P&L)
CREATE TABLE IF NOT EXISTS edinet_controls (
  company_id         UUID    NOT NULL,
  fiscal_year        INTEGER NOT NULL,
  total_assets       NUMERIC,
  total_liabilities  NUMERIC,
  net_assets         NUMERIC,
  revenue            NUMERIC,
  operating_income   NUMERIC,
  net_income         NUMERIC,
  PRIMARY KEY (company_id, fiscal_year)
);

-- Pairwise similarity & novelty (notebook 08_calculate_similarity)
CREATE TABLE IF NOT EXISTS risk_novelty_scores (
  company_id         UUID,
  fiscal_year        INTEGER,
  doc_id_curr        VARCHAR(20),
  doc_id_prev        VARCHAR(20),
  cosine_similarity  DOUBLE PRECISION,
  novelty_score      DOUBLE PRECISION,
  updated_at         TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (company_id, fiscal_year)
);

-- Aggregated change scores (notebook 09_chunk_change_scores)
CREATE TABLE IF NOT EXISTS risk_change_scores (
  company_id         UUID    NOT NULL,
  fiscal_year        INTEGER NOT NULL,
  doc_id_curr        VARCHAR(20),
  doc_id_prev        VARCHAR(20),
  change_mean        DOUBLE PRECISION,
  change_topk        DOUBLE PRECISION,
  change_ratio       DOUBLE PRECISION,
  tau               DOUBLE PRECISION,
  topk_k            INTEGER,
  num_chunks_curr   INTEGER,
  num_chunks_prev   INTEGER,
  text_len_curr     INTEGER,
  text_len_prev     INTEGER,
  max_sim_min       DOUBLE PRECISION,
  max_sim_p10       DOUBLE PRECISION,
  max_sim_median    DOUBLE PRECISION,
  updated_at        TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (company_id, fiscal_year)
);


