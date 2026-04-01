def score(df):
    df = df.sort_values(by='trade_date')

    if len(df) < 15:
        return 0

    score = 0

    close = df['close']
    high = df['high']
    vol = df['vol']

    # 1️⃣ 动量（5日涨幅）
    pct = (close.iloc[-1] / close.iloc[-5] - 1) * 100
    if pct > 5:
        score += 20

    # 2️⃣ 放量
    if vol.iloc[-1] > vol[-5:].mean() * 1.5:
        score += 25

    # 3️⃣ 接近新高
    if close.iloc[-1] >= high[-20:].max() * 0.95:
        score += 25

    # 4️⃣ 均线趋势
    ma5 = close[-5:].mean()
    ma10 = close[-10:].mean()

    if ma5 > ma10:
        score += 15

    # 5️⃣ 连续上涨
    up_days = sum(close.diff().tail(5) > 0)
    if up_days >= 3:
        score += 15

    return score


def is_candidate(score):
    return score >= 60