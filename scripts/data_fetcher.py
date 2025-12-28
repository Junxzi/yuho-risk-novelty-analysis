import os
import zipfile
import requests
from datetime import datetime
from pathlib import Path
import pandas as pd
from dotenv import load_dotenv

# ------------------------
# 設定とユーティリティ
# ------------------------

def load_jquants_credentials():
    load_dotenv()
    return {
        "user": os.getenv("JQUANTS_USER"),
        "password": os.getenv("JQUANTS_PASS"),
        "api_key": os.getenv("JPX_API_KEY"),
    }

def unzip_file(zip_path: str, extract_to: str) -> None:
    """指定したzipファイルを解凍"""
    with zipfile.ZipFile(zip_path, 'r') as zip_ref:
        zip_ref.extractall(extract_to)
    print(f"✅ 解凍完了: {extract_to}")

# ------------------------
# データ取得処理
# ------------------------

def fetch_listed_info(token: str, date_str: str) -> pd.DataFrame:
    """指定日の上場企業情報をJ-Quantsから取得"""
    url = "https://api.jquants.com/v1/listed/info"
    headers = {"Authorization": f"Bearer {token}"}
    params = {"date": date_str}

    response = requests.get(url, headers=headers, params=params)
    response.raise_for_status()

    return pd.DataFrame(response.json().get("info", []))

# ------------------------
# メイン処理
# ------------------------

def fetch_and_save_snapshots(
    start_year: int = 2017,
    end_year: int = datetime.now().year,
    save_dir: str = "../data/raw/topix_growth_snapshots"
) -> None:
    """指定期間の企業スナップショットを取得して保存"""
    creds = load_jquants_credentials()
    token = creds["api_key"]

    save_path = Path(save_dir)
    save_path.mkdir(parents=True, exist_ok=True)

    target_topix = {"TOPIX Core30", "TOPIX Large70", "TOPIX Mid400"}
    target_market = "グロース"

    for year in range(start_year, end_year + 1):
        date_str = f"{year}-11-30"
        try:
            df = fetch_listed_info(token, date_str)
            df_filtered = df[
                (df["ScaleCategory"].isin(target_topix)) |
                (df["MarketCodeName"] == target_market)
            ]

            output_file = save_path / f"{year}_topix_growth.csv"
            df_filtered.to_csv(output_file, index=False)

            print(f"✅ {year}: {len(df_filtered)} 件保存 → {output_file}")
        except Exception as e:
            print(f"⚠️ {year}年の取得に失敗: {e}")