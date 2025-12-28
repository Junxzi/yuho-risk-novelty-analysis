import pandas as pd
import uuid

def load_topix_and_edinet(topix_csv_path: str, edinet_csv_path: str) -> pd.DataFrame:
    """TOPIXとEDINETデータをマージして正規化された企業DataFrameを返す"""

    # データ読み込み
    df_topix = pd.read_csv(topix_csv_path)
    df_edinet = pd.read_csv(edinet_csv_path, encoding="cp932", skiprows=1)

# 証券コードを文字列で統一（zfillで5桁化）
    df_topix["Code"] = df_topix["Code"].astype(str).str.zfill(5)
    df_edinet["証券コード"] = df_edinet["証券コード"].astype(str).str.zfill(5)

    # マージ（証券コードが一致する行）
    df_merged = pd.merge(df_topix, df_edinet, left_on="Code", right_on="証券コード", how="left")

    # --- 欠損補完（会社名でマッチング） ---
    unmatched = df_merged[df_merged["証券コード"].isna()]
    matches = []
    for _, row in unmatched.iterrows():
        name = row["CompanyName"]
        hit = df_edinet[df_edinet["提出者名"].str.contains(name, na=False)]
        if not hit.empty:
            merged_row = row.to_dict()
            merged_row.update(hit.iloc[0].to_dict())
            matches.append(merged_row)
    matched_df = pd.DataFrame(matches)

    # 補完処理
    cols_to_update = list(set(matched_df.columns) & set(df_merged.columns))
    for _, row in matched_df.iterrows():
        company_name = row["CompanyName"]
        for col in cols_to_update:
            mask = (df_merged["CompanyName"] == company_name) & (df_merged[col].isna())
            df_merged.loc[mask, col] = row[col]

    # --- カラム名正規化 ---
    df_merged = df_merged.rename(columns={
        "提出者名": "name_ja",
        "提出者法人番号": "corp_number",
        "ＥＤＩＮＥＴコード": "edinet_code",
        "Code": "security_code",
        "提出者業種": "sector_33",
        "Sector17CodeName": "sector_17",
        "ScaleCategory": "scale_category",
        "MarketCode": "market_code",
        "提出者名（英字）": "name_en",
        "所在地": "address"
    })

    # --- 必要な列抽出 & 型調整 ---
    keep_cols = [
        "security_code", "name_ja", "name_en", "sector_17", "sector_33",
        "scale_category", "market_code", "edinet_code", "address", "corp_number"
    ]
    df_merged = df_merged[keep_cols]

    df_merged["security_code"] = df_merged["security_code"].fillna("").astype(str).str.zfill(5)
    df_merged["edinet_code"] = df_merged["edinet_code"].fillna("").astype(str).str.zfill(6)
    df_merged["corp_number"] = df_merged["corp_number"].apply(
        lambda x: str(int(float(x))).zfill(13) if pd.notnull(x) and x != "" else ""
    )

    # --- UUID付与 ---
    df_merged["company_id"] = [str(uuid.uuid4()) for _ in range(len(df_merged))]

    return df_merged


import pandas as pd

def overwrite_company_ids_if_exists(df: pd.DataFrame, cur) -> pd.DataFrame:
    """
    df に仮割り当てされた company_id を、DB 上の既存 ID（corp_number → edinet_code の順）で上書きする。
    """

    # ① DB から既存 companies をすべて取得
    cur.execute("SELECT company_id, corp_number, edinet_code FROM companies;")
    rows = cur.fetchall()
    db_df = pd.DataFrame(rows, columns=["company_id", "corp_number", "edinet_code"])

    # 型を統一
    for col in ["corp_number", "edinet_code"]:
        df[col] = df[col].astype(str).fillna("")
        db_df[col] = db_df[col].astype(str).fillna("")

    # ② corp_number でマージ（最優先）
    df = df.merge(
        db_df[["corp_number", "company_id"]],
        how="left", on="corp_number", suffixes=("", "_from_corp")
    )
    if "company_id_from_corp" in df.columns:
        df["company_id"] = df["company_id_from_corp"].combine_first(df.get("company_id"))
        df = df.drop(columns=["company_id_from_corp"])

    # ③ edinet_code でマージ（corp_number でマッチしなかったものに限り）
    df = df.merge(
        db_df[["edinet_code", "company_id"]],
        how="left", on="edinet_code", suffixes=("", "_from_edinet")
    )
    if "company_id_from_edinet" in df.columns:
        df["company_id"] = df["company_id_from_edinet"].combine_first(df.get("company_id"))
        df = df.drop(columns=["company_id_from_edinet"])

    # ④ UUID が欠けている行に新しく UUID を発行（これは最後の手段）
    def ensure_uuid(val):
        if pd.isna(val) or val == "":
            return str(uuid.uuid4())
        return val

    df["company_id"] = df["company_id"].apply(ensure_uuid)

    return df