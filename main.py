import os
import time
import requests
import pandas as pd
from telegram import Bot
from config import *

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ---------- API SAFE ----------
def fetch(symbol, interval="1min"):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={TWELVE_DATA_KEY}&outputsize=30"
    r = requests.get(url).json()

    if "values" not in r:
        return None

    df = pd.DataFrame(r["values"])[::-1]
    df["close"] = df["close"].astype(float)
    df["volume"] = df["volume"].astype(float)
    return df

# ---------- INDICATORS ----------
def indicators(df):
    df["ema5"] = df["close"].ewm(span=5).mean()
    df["ema20"] = df["close"].ewm(span=20).mean()
    df["vwap"] = (df["close"] * df["volume"]).cumsum() / df["volume"].cumsum()
    return df

# ---------- SCANNER (خفيف) ----------
def scan_market():
    candidates = []

    for s in STOCKS:
        df = fetch(s, "1min")
        if df is None or len(df) < 10:
            continue

        df = indicators(df)
        last = df.iloc[-1]

        # فلترة سريعة جدًا
        if last["volume"] > df["volume"].mean() * 1.5:
            if abs(last["close"] - last["vwap"]) / last["vwap"] < 0.01:
                candidates.append(s)

    return candidates

# ---------- ANALYZER (ثقيل) ----------
def analyze(symbol):
    df1 = fetch(symbol, "1min")
    df5 = fetch(symbol, "5min")
    df15 = fetch(symbol, "15min")

    if df1 is None or df5 is None or df15 is None:
        return None

    df1 = indicators(df1)
    df5 = indicators(df5)
    df15 = indicators(df15)

    a = df1.iloc[-1]
    b = df5.iloc[-1]
    c = df15.iloc[-1]

    # BUY
    if (
        a["close"] > a["vwap"] and
        a["ema5"] > a["ema20"] and
        b["ema5"] > b["ema20"] and
        c["ema5"] > c["ema20"]
    ):
        return {
            "symbol": symbol,
            "type": "BUY",
            "entry": a["close"],
            "sl": a["close"] * 0.995,
            "tp": a["close"] * 1.02
        }

    # SELL
    if (
        a["close"] < a["vwap"] and
        a["ema5"] < a["ema20"] and
        b["ema5"] < b["ema20"] and
        c["ema5"] < c["ema20"]
    ):
        return {
            "symbol": symbol,
            "type": "SELL",
            "entry": a["close"],
            "sl": a["close"] * 1.005,
            "tp": a["close"] * 0.98
        }

    return None

# ---------- SEND ----------
def send(alert):
    msg = f"""
🚀 {alert['type']} SIGNAL
Stock: {alert['symbol']}
Entry: {alert['entry']}
SL: {alert['sl']}
TP: {alert['tp']}
"""
    bot.send_message(TELEGRAM_CHAT_ID, msg)

# ---------- LOOP ----------
while True:
    try:
        print("Scanning market...")
        candidates = scan_market()

        print("Candidates:", candidates)

        for c in candidates:
            result = analyze(c)
            if result:
                send(result)

        time.sleep(CHECK_INTERVAL)

    except Exception as e:
        print("Error:", e)
        time.sleep(10)
