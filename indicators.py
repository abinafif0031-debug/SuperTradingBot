import pandas_ta as ta
import pandas as pd

def add_all_indicators(df):
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

    # محاولة استخدام الاسمين المتاحين
    try:
        engulf = ta.cdl_pattern(df['open'], df['high'], df['low'], df['close'], name='cdl_engulfing')
        if engulf is None:
            raise ValueError
    except:
        engulf = ta.cdl_pattern(df['open'], df['high'], df['low'], df['close'], name='CDLENGULFING')
    df['bull_engulf'] = (engulf > 0) if engulf is not None else False
    return df

def add_emas(df, periods=[20,50]):
    if not isinstance(df.index, pd.DatetimeIndex):
        df = df.set_index('date')
    df = df.sort_index()
    for p in periods:
        df[f'EMA{p}'] = ta.ema(df['close'], length=p)
    return df
