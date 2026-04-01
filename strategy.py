def is_limit_up(df):
    df = df.sort_values(by='trade_date')

    if len(df) < 2:
        return False

    # 昨日涨幅
    pct = (df['close'].iloc[-2] / df['close'].iloc[-3] - 1) * 100

    # 👉 接近涨停（A股约10%）
    return pct > 8


def strong_stock(df):
    df = df.sort_values(by='trade_date')

    # 今日继续强势
    pct_today = (df['close'].iloc[-1] / df['close'].iloc[-2] - 1) * 100

    return pct_today > 2