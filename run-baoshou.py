import pandas as pd
from notify import send


def filter_stock(code):
    return not (code.startswith('300') or code.startswith('688'))


def main():
    df_all = pd.read_csv("all_stock.csv")

    print("股票数量:", df_all['ts_code'].nunique())

    results = []

    for code, df in df_all.groupby('ts_code'):

        if not filter_stock(code):
            continue

        if len(df) < 5:
            continue

        df = df.sort_values(by='trade_date').copy()
        df = df.dropna(subset=['close', 'vol'])

        if len(df) < 5:
            continue

        close = df['close']
        vol = df['vol']
        high = df['high']

        # ==============================
        # 核心指标
        # ==============================
        pct = close.pct_change()

        pct1 = pct.iloc[-1]   # 今天
        pct2 = pct.iloc[-2]   # 昨天
        pct3 = (close.iloc[-1] / close.iloc[-3]) - 1
        pct5 = (close.iloc[-1] / close.iloc[0]) - 1

        vol_ma3 = vol.rolling(3).mean().iloc[-1]
        vol_ratio = vol.iloc[-1] / (vol_ma3 + 1e-6)

        high_5 = high.max()

        score = 0

        # ==============================
        # 🔥 1️⃣ “突变”（最核心！！！）
        # ==============================
        # 昨天弱，今天突然强
        if pct2 < 0 and pct1 > 0.02:
            score += 40

        # 今天明显转强
        if pct1 > 0.04:
            score += 30

        # ==============================
        # 🔥 2️⃣ “突然放量”（主力进场）
        # ==============================
        if vol_ratio > 2.5:
            score += 40
        elif vol_ratio > 1.8:
            score += 25

        # ==============================
        # 🔥 3️⃣ “低位异动”（重点）
        # ==============================
        if pct5 < 0.08:
            score += 30   # 还没涨 → 最容易连板

        # ==============================
        # 🔥 4️⃣ “开始加速”
        # ==============================
        if pct3 > 0.04:
            score += 20

        # ==============================
        # 🔥 5️⃣ “突破临界”
        # ==============================
        if close.iloc[-1] >= high_5 * 0.93:
            score += 25

        # ==============================
        # ❗ 反向信号（极弱才扣）
        # ==============================
        if pct1 < -0.02:
            score -= 20

        # ==============================
        # 🔥 极激进分级
        # ==============================
        if score >= 85:
            level = "🔥点火龙头"
        elif score >= 65:
            level = "⚡资金试盘"
        elif score >= 50:
            level = "🪤潜伏标的"
        else:
            continue

        results.append((code, score, level))

    if not results:
        print("⚠️ 无结果（极端冰点行情）")
        return

    results.sort(key=lambda x: x[1], reverse=True)

    msg = "🚀 点火龙头候选（极激进版）：\n\n"

    for code, s, lv in results[:15]:
        msg += f"{code} ⭐ {s} | {lv}\n"

    print(msg)

    send(msg)


if __name__ == "__main__":
    main()