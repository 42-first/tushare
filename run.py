import pandas as pd
from model import score
from strategy import limit_up_potential
from notify import send


def main():
    df_all = pd.read_csv("all_stock.csv")

    results = []

    # ==============================
    # 🔥 按股票分组
    # ==============================
    for code, df in df_all.groupby('ts_code'):

        if len(df) < 20:
            continue

        df = df.sort_values(by='trade_date')

        # ==============================
        # 🔥 评分（核心）
        # ==============================
        base_score = score(df)
        strategy_score = limit_up_potential(df)

        final_score = base_score + strategy_score

        results.append((code, final_score))

    # ==============================
    # 🔥 排序
    # ==============================
    results.sort(key=lambda x: x[1], reverse=True)

    # ==============================
    # 🔥 输出
    # ==============================
    msg = "🔥 今日涨停潜力股（Top10）：\n\n"

    for code, s in results[:10]:
        msg += f"{code} ⭐ {s}\n"

    print(msg)

    if results:
        send(msg)


if __name__ == "__main__":
    main()