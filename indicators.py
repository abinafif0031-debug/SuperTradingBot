import pandas_ta as ta

def add_all_indicators(df):
    # لا نضبط الفهرس هنا، نفترض أن df يحتوي على DatetimeIndex وجميع الأعمدة
    df['RSI'] = ta.rsi(df['close'], length=14)
    macd = ta.macd(df['close'])
    df['MACD_line'] = macd['MACD_12_26_9']
    df['MACD_signal'] = macd['MACDs_12_26_9']
    df['ATR'] = ta.atr(df['high'], df['low'], df['close'], length=14)
    df['VWAP'] = ta.vwap(df['high'], df['low'], df['close'], df['volume'])
    df['vol_avg'] = df['volume'].rolling(20).mean()
    df['vol_ratio'] = df['volume'] / df['vol_avg']
    df['CMF'] = ta.cmf(df['high'], df['low'], df['close'], df['volume'], length=20)
    # نعطل نموذج الشمعة مؤقتاً (غير متاح)
    df['bull_engulf'] = False
    return df

def add_emas(df, periods=[20,50]):
    # لا نضبط الفهرس هنا أيضاً
    for p in periods:
        df[f'EMA{p}'] = ta.ema(df['close'], length=p)
    return df
