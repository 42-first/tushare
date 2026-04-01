def limit_up_potential(df):
    score = 0

    close = df['close']
    vol = df['vol']

    # ==============================
    # 1️⃣ 成交量温和放大（关键）
    # ==============================
    vol_ma5 = vol.rolling(5).mean().iloc[-1]
    vol_ratio = vol.iloc[-1] / (vol_ma5 + 1e-6)

    if 1.2 < vol_ratio < 2:
        score += 25

    # ==============================
    # 2️⃣ 涨幅不过热（提前发现）
    # ==============================
    pct = close.pct_change().iloc[-1]

    if 0.02 < pct < 0.07:
        score += 20

    return score


# 🔥 龙头识别（核心）
def leader_score(df):
    score = 0

    close = df['close']
    vol = df['vol']

    # ==============================
    # 1️⃣ 强势上涨
    # ==============================
    pct_3 = (close.iloc[-1] / close.iloc[-3]) - 1

    if pct_3 > 0.12:
        score += 25
    elif pct_3 > 0.06:
        score += 15

    # ==============================
    # 2️⃣ 放量（主力进场）
    # ==============================
    vol_ma5 = vol.rolling(5).mean().iloc[-1]
    vol_ratio = vol.iloc[-1] / (vol_ma5 + 1e-6)

    if vol_ratio > 1.5:
        score += 20

    # ==============================
    # 3️⃣ 接近新高（龙头特征）
    # ==============================
    high_20 = df['high'].rolling(20).max().iloc[-1]

    if close.iloc[-1] >= high_20 * 0.95:
        score += 20

    # ==============================
    # 4️⃣ 连续上涨
    # ==============================
    pct = close.pct_change()

    if (pct.iloc[-3:] > 0).all():
        score += 15

    return score