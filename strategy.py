def limit_up_potential(df):
    score = 0

    close = df['close']
    vol = df['vol']

    # ===== 成交量温和放大 =====
    vol_ma5 = vol.rolling(5).mean().iloc[-1]
    vol_ratio = vol.iloc[-1] / vol_ma5

    if 1.2 < vol_ratio < 2:
        score += 15

    # ===== 连续小阳线 =====
    df['pct'] = close.pct_change()
    recent = df['pct'].iloc[-3:]

    if (recent > 0).sum() >= 2 and recent.iloc[-1] < 0.05:
        score += 15

    # ===== 均线金叉 =====
    ma5 = close.rolling(5).mean()
    ma10 = close.rolling(10).mean()

    if ma5.iloc[-2] < ma10.iloc[-2] and ma5.iloc[-1] > ma10.iloc[-1]:
        score += 20

    # ===== 刚脱离底部 =====
    low_10 = df['low'].rolling(10).min()

    if close.iloc[-1] > low_10.iloc[-1] * 1.05:
        score += 10

    return score