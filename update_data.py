import tushare as ts
import pandas as pd
import os
import datetime
import time
from config import TUSHARE_TOKEN

ts.set_token(TUSHARE_TOKEN)
pro = ts.pro_api()

DATA_FILE = "all_stock.csv"


# ==============================
# 🔥 自己生成日期（关键）
# ==============================
def get_recent_dates(days=40):
    today = datetime.datetime.today()
    dates = []

    for i in range(days):
        d = today - datetime.timedelta(days=i)
        dates.append(d.strftime("%Y%m%d"))

    return dates


# ==============================
# 🔥 自动识别交易日
# ==============================
def get_trade_dates(n=20):
    dates = get_recent_dates(40)

    trade_dates = []

    for d in dates:
        try:
            df = pro.daily(trade_date=d)

            # 👉 有数据 = 交易日
            if df is not None and not df.empty:
                trade_dates.append(d)
                print("✅ 交易日:", d)

            time.sleep(0.5)

        except Exception:
            continue

        if len(trade_dates) >= n:
            break

    return trade_dates[::-1]  # 正序


# ==============================
# 🔥 主逻辑
# ==============================
def update():
    trade_dates = get_trade_dates(20)

    print("📅 最终交易日:", trade_dates)

    all_data = []

    for date in trade_dates:
        print("📥 拉取:", date)

        try:
            df = pro.daily(trade_date=date)

            # ❌ 过滤创业板 + 科创板 + 北交所
            df = df[~df['ts_code'].str.startswith(('30', '68', '920'))]

            all_data.append(df)

            time.sleep(0.6)

        except Exception as e:
            print("❌ 失败:", e)
            time.sleep(2)

    df_all = pd.concat(all_data)

    df_all = df_all.sort_values(by=['ts_code', 'trade_date'])

    df_all.to_csv(DATA_FILE, index=False)

    print("✅ 完成:", len(df_all))


if __name__ == "__main__":
    update()