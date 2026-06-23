import time
import requests
import pandas as pd
import numpy as np
from datetime import datetime
from telegram import Bot
from config import TELEGRAM_BOT_TOKEN, TELEGRAM_CHAT_ID, TWELVE_DATA_KEY, FINNHUB_API_KEY, ANTHROPIC_API_KEY, CHECK_INTERVAL_MIN, STOCKS

bot = Bot(token=TELEGRAM_BOT_TOKEN)

# ---------- حساب المؤشرات ----------
def compute_indicators(df):
    df['close'] = df['close'].astype(float)
    df['volume'] = df['volume'].astype(float)
    df['EMA5'] = df['close'].ewm(span=5, adjust=False).mean()
    df['EMA20'] = df['close'].ewm(span=20, adjust=False).mean()
    df['VWAP'] = (df['close'] * df['volume']).cumsum() / df['volume'].cumsum()
    df['RSI'] = 100 - (100 / (1 + df['close'].diff().apply(lambda x: max(x,0)).rolling(14).mean() /
                               df['close'].diff().apply(lambda x: abs(min(x,0))).rolling(14).mean()))
    return df

# ---------- جلب البيانات لكل سهم ----------
def get_stock_data(symbol, interval):
    url = f"https://api.twelvedata.com/time_series?symbol={symbol}&interval={interval}&apikey={TWELVE_DATA_KEY}&outputsize=50"
    data = requests.get(url).json()
    df = pd.DataFrame(data['values'])[::-1]
    return compute_indicators(df)

# ---------- فلترة أخبار Finnhub ----------
def check_finnhub_news(symbol):
    url = f"https://finnhub.io/api/v1/stock/news?symbol={symbol}&token={FINNHUB_API_KEY}"
    news = requests.get(url).json()
    for item in news:
        if item.get("related") and symbol in item["related"]:
            return True
    return False

# ---------- التحقق من الإشارة ----------
def check_signal(symbol):
    df_1m = get_stock_data(symbol, "1min")
    df_5m = get_stock_data(symbol, "5min")
    df_15m = get_stock_data(symbol, "15min")

    latest_1m = df_1m.iloc[-1]
    latest_5m = df_5m.iloc[-1]
    latest_15m = df_15m.iloc[-1]

    # إشارات شراء
    if (latest_1m['close'] > latest_1m['VWAP'] and latest_1m['EMA5'] > latest_1m['EMA20'] and latest_1m['RSI'] < 70 and
        latest_5m['EMA5'] > latest_5m['EMA20'] and latest_15m['EMA5'] > latest_15m['EMA20']):
        entry = latest_1m['close']
        stop_loss = entry * 0.995
        take_profit = entry * 1.02
        signal = "Strong BUY"

    # إشارات بيع
    elif (latest_1m['close'] < latest_1m['VWAP'] and latest_1m['EMA5'] < latest_1m['EMA20'] and latest_1m['RSI'] > 30 and
          latest_5m['EMA5'] < latest_5m['EMA20'] and latest_15m['EMA5'] < latest_15m['EMA20']):
        entry = latest_1m['close']
        stop_loss = entry * 1.005
        take_profit = entry * 0.98
        signal = "Strong SELL"
    else:
        return None

    # فلترة الأخبار
    if check_finnhub_news(symbol):
        return None

    return {
        "symbol": symbol,
        "signal": signal,
        "entry": entry,
        "stop_loss": stop_loss,
        "take_profit": take_profit,
        "time": datetime.now().strftime("%H:%M:%S")
    }

# ---------- إرسال Telegram ----------
def send_telegram(alert):
    message = f"""
🚀 {alert['signal']} Alert: {alert['symbol']}
Entry: {alert['entry']:.2f} USD
Stop Loss: {alert['stop_loss']:.2f}
Take Profit: {alert['take_profit']:.2f}
Time: {alert['time']}
"""
    bot.send_message(chat_id=TELEGRAM_CHAT_ID, text=message)

# ---------- تشغيل البوت ----------
while True:
    for symbol in STOCKS:
        alert = check_signal(symbol)
        if alert:
            send_telegram(alert)
    time.sleep(CHECK_INTERVAL_MIN * 60)