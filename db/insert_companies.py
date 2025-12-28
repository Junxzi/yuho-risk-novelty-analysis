# src/db/insert_companies.py
import pandas as pd
from db.connection import get_connection
from psycopg2.extras import execute_values

def insert_companies_from_csv(csv_path: str):
    df = pd.read_csv(csv_path)

    # 欠損を文字列で置換（NaNはPostgreSQLでNULLとして処理）
    df = df.fillna("")

    records = [
        (
            str(row["証券コード"]),
            row["ＥＤＩＮＥＴコード"],
            row["提出者名"],
            row.get("提出者名（英字）", ""),
            row.get("提出者名（ヨミ）", ""),
            row["所在地"],
            str(int(row["提出者法人番号"])) if row["提出者法人番号"] != "" else None,
            row.get("Sector17Code", ""),
            row.get("Sector17CodeName", ""),
            row.get("Sector33Code", ""),
            row.get("Sector33CodeName", "")
        )
        for _, row in df.iterrows()
        if pd.notnull(row["証券コード"])  # 証券コードがないものはスキップ
    ]

    insert_sql = """
        INSERT INTO companies (
            securities_code,
            edinet_code,
            company_name,
            company_name_en,
            company_name_kana,
            address,
            corporate_number,
            sector17_code,
            sector17_name,
            sector33_code,
            sector33_name
        )
        VALUES %s
        ON CONFLICT (securities_code)
        DO UPDATE SET
            edinet_code = EXCLUDED.edinet_code,
            company_name = EXCLUDED.company_name,
            company_name_en = EXCLUDED.company_name_en,
            company_name_kana = EXCLUDED.company_name_kana,
            address = EXCLUDED.address,
            corporate_number = EXCLUDED.corporate_number,
            sector17_code = EXCLUDED.sector17_code,
            sector17_name = EXCLUDED.sector17_name,
            sector33_code = EXCLUDED.sector33_code,
            sector33_name = EXCLUDED.sector33_name,
            updated_at = NOW()
    """

    with get_connection() as conn:
        with conn.cursor() as cur:
            execute_values(cur, insert_sql, records)
        conn.commit()

    print(f"✅ {len(records)} 件の企業情報を upsert 済み")