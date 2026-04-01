import pandas as pd

def score(df):
    df = df.copy()

    if len(df) < 20:
        return 0

    close = df['close']

    score = 0

    # ==============================
    # 1️⃣ 均线多头（提前信号）
    # ==============================
    ma5 = close.rolling(5).mean().iloc[-1]
    ma10 = close.rolling(10).mean().iloc[-1]
    ma20 = close.rolling(20).mean().iloc[-1]

    if ma5 > ma10 > ma20:
        score += 15

    # ==============================
    # 2️⃣ 温和上涨（避免追高）
    # ==============================
    pct_5 = (close.iloc[-1] / close.iloc[-5]) - 1

    if 0.03 < pct_5 < 0.15:
        score += 20

    # ==============================
    # 3️⃣ 波动收敛（启动前特征）
    # ==============================
    std = close.pct_change().rolling(5).std().iloc[-1]

    if std < 0.02:
        score += 10

    return score