## 再現性レポジトリ（日本株：リスク開示の新規性 × 市場反応）

本リポジトリは、卒業研究論文で用いた実証パイプラインを**第三者が追試できる形**でまとめたものです。

- EDINET 有価証券報告書 → 「事業等のリスク」欄の抽出
- 埋め込み（sentence-transformers）＋コサイン類似度に基づく **新規性 / 変化度** 指標の構築
- 提出日をイベント日とするイベントスタディ（異常出来高、CAR、\(\sum \lvert AR \rvert\) 等）
- 回帰分析と頑健性検証（プレトレンド、偽イベント日プラセボ等）

### 含まれるもの / 含まれないもの
- **含まれるもの**：ノートブック、スクリプト、DBスキーマ（`sql/`）、依存関係（`requirements.txt`）。
- **含まれないもの**：生データや巨大な中間生成物（`.gitignore`参照）。  
  データの利用条件・容量の都合により、**`data/` と `outputs/` は同梱しません**。

### クイックスタート（DB + Python）

### 動作確認済みPythonバージョン
- **Python 3.10.18**（ノートブック作成時の環境。再現の際は同系統の 3.10.x を推奨）

1) **`.env` を作成**

リポジトリ直下に `.env` を作ります（雛形：`config/env.example`）。

cp config/env.example .env2) **PostgreSQL を起動**

2) **PostgreSQL を起動**

3) **Python 依存関係をインストール**

初回起動時に `sql/001_schema.sql` によりテーブルが作成されます。

3) **Python 依存関係をインストール**

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt4) **ノートブック実行（推奨順）**

- `notebooks/02_fetch_yuho.ipynb`：EDINET書類メタデータの登録（`edinet_documents`）
- `notebooks/03_extract_risk_section.ipynb`：「事業等のリスク」欄の抽出（ローカル保存）
- `notebooks/04_upsert_risk_section.ipynb`：抽出結果をDBへ反映（`risk_text`）
- `notebooks/06_fetch_control_variable_elements.ipynb`：統制変数（財務項目）の抽出・登録
- `notebooks/08_calculate_similarity.ipynb`：類似度・新規性の算出（ペア）
- `notebooks/09_chunk_change_scores.ipynb`：集約指標（例：`change_topk`）の作成
- `notebooks/10_event_study_market_model.ipynb` / `11_event_study_uncertainty.ipynb`：イベント窓アウトカム算出
- `notebooks/14_results_writeup.ipynb`：最終結果（表・図の生成）

4) **ノートブック実行（推奨順）**

- `notebooks/02_fetch_yuho.ipynb`：EDINET書類メタデータの登録（`edinet_documents`）
- `notebooks/03_extract_risk_section.ipynb`：「事業等のリスク」欄の抽出（ローカル保存）
- `notebooks/04_upsert_risk_section.ipynb`：抽出結果をDBへ反映（`risk_text`）
- `notebooks/06_fetch_control_variable_elements.ipynb`：統制変数（財務項目）の抽出・登録
- `notebooks/08_calculate_similarity.ipynb`：類似度・新規性の算出（ペア）
- `notebooks/09_chunk_change_scores.ipynb`：集約指標（例：`change_topk`）の作成
- `notebooks/10_event_study_market_model.ipynb` / `11_event_study_uncertainty.ipynb`：イベント窓アウトカム算出
- `notebooks/14_results_writeup.ipynb`：最終結果（表・図の生成）

### 認証情報・データ入手に関する注意
- EDINET由来データ、および株価・財務データは取得元の利用条件に従って別途準備してください。
- J-Quants を用いる場合は `.env` に `JPX_API_KEY` / `JQUANTS_USER` / `JQUANTS_PASS` を設定してください（必要なノートブックのみ）。

---

## (Optional) English summary

This repository contains notebooks/scripts to reproduce the thesis pipeline (Japan, EDINET risk disclosures → embedding-based novelty → event-study outcomes → regressions).  
Raw data and large artifacts are excluded; see `.gitignore`. Please follow the Quickstart section above (Japanese) for setup and notebook execution order.

This repository contains notebooks/scripts to reproduce the thesis pipeline (Japan, EDINET risk disclosures → embedding-based novelty → event-study outcomes → regressions).  
Raw data and large artifacts are excluded; see `.gitignore`. Please follow the Quickstart section above (Japanese) for setup and notebook execution order.
