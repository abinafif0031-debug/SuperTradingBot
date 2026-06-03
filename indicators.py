import pandas_ta as ta

def add_all_indicators(df):
    # تأكد من أن الفهرس زمني ومرتب
    if not isinstance(df.index, pd.DatetimeIndex):
        df = df.set_index('date')
    df = df.sort_index()

    df['RSI'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    df['MACD_line'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    df['VWAP'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
    df['vol_avg'] = df['volume'].rolling(20).mean()
    df['vol_ratio'] = df['volume'] / df['vol_avg']
    df['CMF'] = ta.cmf(df['high'], df['low'], df['close'], df['volume'], length=20)
    # اسم النموذج الصحيح
    engulfing = ta.cdl_pattern(df['open'], df['high'], df['low'], df['close'], name='cdl_engulfing')
    if engulfing is not None:
        df['bull_engulf'] = engulfing > 0
    else:
        # استخدام الاسم البديل
        engulfing = ta.cdl_pattern(df['open'], df['high'], df['low'], df['close'], name='CDLENGULFING')
        if engulfing is not None:
            df['bull_engulf'] = engulfing > 0
        else:
            df['bull_engulf'] = False
    return df

def add_emas(df, periods=[20,50]):
    if not isinstance(df.index, pd.DatetimeIndex):
        df = df.set_index('date')
    df = df.sort_index()
    for p in periods:
        df[f'EMA{p}'] = ta.ema(df['close'], length=p)
    return df
