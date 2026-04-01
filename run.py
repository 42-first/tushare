import pandas as pd
from model import score
from strategy import is_limit_up, strong_stock
from notify import send


def main():
    df_all = pd.read_csv("all_stock.csv")

    results = []

    # ==============================
    # 🔥 按股票分组（关键）
    # ==============================
    for code, df in df_all.groupby('ts_code'):

        if len(df) < 20:
            continue

        df = df.sort_values(by='trade_date')

        # 👉 打标签
        limit_flag = is_limit_up(df)
        strong_flag = strong_stock(df)

        base_score = score(df)

        final_score = base_score

        if limit_flag:
            final_score += 20

        if strong_flag:
            final_score += 10

        results.append((code, final_score, limit_flag, strong_flag))

    # ==============================
    # 🔥 排序
    # ==============================
    results.sort(key=lambda x: x[1], reverse=True)

    # ==============================
    # 🔥 输出
    # ==============================
    msg = "🔥 今日涨停潜力股（Top10）：\n\n"

    for code, s, l, st in results[:10]:
        msg += f"{code} ⭐ {s} | 涨停:{l} 强势:{st}\n"

    print(msg)

    if results:
        send(msg)


if __name__ == "__main__":
    main()