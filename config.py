import os
from dotenv import load_dotenv
load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
FINNHUB_API_KEY = os.getenv("FINNHUB_API_KEY")
ALPHA_VANTAGE_KEY = os.getenv("ALPHA_VANTAGE_KEY")
TWELVE_DATA_KEY = os.getenv("TWELVE_DATA_KEY")
OPTIONWHALES_KEY = os.getenv("OPTIONWHALES_KEY")
ADMIN_CHAT_ID = int(os.getenv("ADMIN_CHAT_ID", "0"))

# قائمة الأسهم – ابدأ بـ 10 أسهم فقط للتجربة، ثم وسّع بعد ما تتأكد إن كل شيء شغال
SYMBOLS = [
    # Tech - Semiconductors
    "NVDA", "AMD", "QCOM", "AVGO", "TXN", "MU", "AMAT", "LRCX", "KLAC",
    "MRVL", "ADI", "INTC", "ON", "MCHP", "MPWR", "ENTG", "ONTO", "SWKS",
    # Tech - Hardware
    "AAPL", "MSFT", "DELL", "PSTG", "NTAP", "HPE",
    # Software / SaaS
    "GOOGL", "META", "ADBE", "CRM", "NOW", "ORCL", "TEAM", "DDOG", "SNOW",
    "NET", "CRWD", "ZS", "HUBS", "WDAY", "VEEV", "MDB", "CFLT", "GTLB",
    "ZM", "DOCU", "BILL", "PAYC", "NTNX", "ESTC",
    # AI / Data
    "PLTR", "AI", "SOUN", "BBAI", "TTD", "APP", "IONQ", "QBTS", "RGTI", "RXRX",
    # E-Commerce
    "AMZN", "SHOP", "MELI", "SE", "EBAY", "ETSY", "CPNG", "PDD",
    # EVs
    "TSLA", "RIVN", "LCID", "NIO", "XPEV", "LI",
    # Clean Energy
    "ENPH", "SEDG", "FSLR", "RUN", "ARRY", "NOVA", "PLUG", "BE", "STEM", "NEE",
    # Healthcare - Devices
    "ABT", "TMO", "DHR", "MDT", "BSX", "SYK", "ISRG", "IDXX", "ALGN", "DXCM",
    "PODD", "HOLX", "ZBH", "NTRA", "ILMN", "IRTC",
    # Industrial
    "CAT", "DE", "EMR", "ROK", "PH", "ITW", "CMI", "PCAR", "WAB", "FAST",
    # Consumer
    "COST", "HD", "LOW", "TGT", "ROST", "TJX", "ULTA", "LULU", "NKE", "CMG", "YUM",
    # Payments (Fintech)
    "V", "MA", "PYPL", "SQ", "FIS", "FISV",
    # Travel
    "UBER", "LYFT", "ABNB", "BKNG", "EXPE",
    # Telecom / Social
    "TMUS", "CHTR", "PINS", "SNAP", "SPOT",
    # Biotech
    "AMGN", "GILD", "REGN", "VRTX", "ALNY", "CRSP",
    # ETFs for market context
    "SPY", "QQQ"
]
