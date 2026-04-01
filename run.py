import pandas as pd
from model import score
from strategy import limit_up_potential, leader_score
from notify import send


def filter_stock(code):
    return not (code.startswith('300') or code.startswith('688'))


def get_sector(code):
    if code.startswith('600') or code.startswith('601'):
        return '主板'
    elif code.startswith('000'):
        return '深主板'
    elif code.startswith('002'):
        return '中小板'
    else:
        return '其他'


def main():
    df_all = pd.read_csv("all_stock.csv")

    print("股票数量:", df_all['ts_code'].nunique())

    stock_scores = []

    for code, df in df_all.groupby('ts_code'):

        if not filter_stock(code):
            continue

        # if len(df) < 30:
        #     continue

        df = df.sort_values(by='trade_date').copy()
        df = df.dropna(subset=['close', 'vol'])

        if len(df) < 20:
            continue

        close = df['close']
        vol = df['vol']

        # ==============================
        # 🔥 硬过滤（关键）
        # ==============================
        vol_ma5 = vol.rolling(5).mean().iloc[-1]
        vol_ratio = vol.iloc[-1] / (vol_ma5 + 1e-6)

        if vol_ratio < 1.2:
            continue

        if close.iloc[-1] < close.iloc[-5]:
            continue

        # ==============================
        # 👉 原始评分
        # ==============================
        base = score(df)
        potential = limit_up_potential(df)
        leader = leader_score(df)

        total = base + potential + leader

        # ==============================
        # 🔥 爆发因子（拉开差距）
        # ==============================
        pct1 = close.pct_change().iloc[-1]
        pct3 = (close.iloc[-1] / close.iloc[-3]) - 1

        if pct1 > 0.05:
            total += 20

        if pct3 > 0.12:
            total += 30

        # ==============================
        # ❗ 淘汰机制
        # ==============================
        if total < 60:
            continue

        sector = get_sector(code)

        stock_scores.append((code, sector, round(total, 2)))

    if not stock_scores:
        print("⚠️ 无结果（说明市场很弱 or 条件过严）")
        return

    # ==============================
    # 🔥 板块选龙头
    # ==============================
    sector_map = {}

    for code, sector, s in stock_scores:
        sector_map.setdefault(sector, []).append((code, s))

    leaders = []

    for sector, stocks in sector_map.items():
        stocks.sort(key=lambda x: x[1], reverse=True)

        leaders.extend([(code, s, sector) for code, s in stocks[:2]])

    leaders.sort(key=lambda x: x[1], reverse=True)

    # ==============================
    # 输出
    # ==============================
    msg = "🔥 今日龙头候选（强化版）：\n\n"

    for code, s, sec in leaders[:10]:
        msg += f"{code} ⭐ {s} | {sec}\n"

    print(msg)

    if leaders:
        send(msg)


if __name__ == "__main__":
    main()