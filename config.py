import os

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
TELEGRAM_CHAT_ID = os.getenv("TELEGRAM_CHAT_ID")

TWELVE_DATA_KEY = os.getenv("TWELVE_DATA_KEY")

CHECK_INTERVAL = 180  # 3 دقائق

STOCKS = [
    "AMD",
    "AAPL","MSFT","AMZN","GOOGL","NVDA","META","TSLA","LLY","ABBV","PFE",
    "MRK","TMO","ABT","DHR","BMY","MDT","GILD","CAT","DE","MMM",
    "ETN","HON","GE","PCAR","EMR","ROP","ADI","COST","WMT","HD",
    "NKE","LOW","CVS","TGT","BKNG","SBUX","DG","NFLX","ATVI","EA",
    "TTWO","DIS","VZ","T","TMUS","CHTR","CMCSA","PPG","SHW","ECL",
    "CUM","ROK","ITW","PH","SWK","FAST","ZTS","SYK","HCA","LH",
    "DGX","CNC","HUM","EW","REGN","ISRG","BDX","V","MA","PYPL",
    "SQ","AXP","SCHW","CME","ICE","BLK","INTU","ADBE","CSCO","MSCI",
    "TJX","KR","DLTR","ROST","AZO","ORLY","GPC","KMX","TSCO"
    # أكمل الباقي لتصل 140 سهم
]
