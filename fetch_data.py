import requests
import pandas as pd
import os
import sys
from datetime import datetime

def fetch_twse_data():
    # 取得當前日期 (格式: 20260317)
    # 注意：GitHub Action 運行在 UTC 時間，晚點我們在 yml 設定時區
    target_date = datetime.now().strftime("%Y%m%d")
    url = f"https://www.twse.com.tw/rwd/zh/TAIEX/MI_5MINS_INDEX?response=json&date={target_date}"

    headers = {
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/145.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest'
    }

    try:
        response = requests.get(url, headers=headers, timeout=15)
        result = response.json()

        if result.get("stat") == "OK":
            df = pd.DataFrame(result["data"], columns=result["fields"])
            
            # 數值清理
            numeric_cols = df.columns[1:]
            for col in numeric_cols:
                df[col] = df[col].str.replace(',', '').astype(float)
            
            df.insert(0, '日期', result["date"])

            # 確保 data 目錄存在
            os.makedirs('data', exist_ok=True)
            
            # 儲存檔案
            file_path = f"data/{target_date}.csv"
            df.to_csv(file_path, index=False, encoding="utf-8-sig")
            print(f"成功儲存檔案: {file_path}")
            
        else:
            print(f"當前日期 ({target_date}) 無資料：{result.get('stat')}")
            # 正常結束，但不執行後續 push
            sys.exit(0)

    except Exception as e:
        print(f"發生錯誤: {e}")
        sys.exit(1) # 回傳錯誤代碼，讓 Action 顯示失敗

if __name__ == "__main__":
    fetch_twse_data()