import asyncio
import logging
from aiohttp import web
from config import TELEGRAM_BOT_TOKEN, SYMBOLS, ADMIN_CHAT_ID
from data_feeds import MarketData
from signal_generator import SignalGenerator
from trade_manager import TradeManager
from beast_engine.adaptive_learner import init_db
import bot_handlers

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

async def health_check(request):
    return web.Response(text="OK")

async def run_web_server():
    app = web.Application()
    app.router.add_get('/', health_check)
    runner = web.AppRunner(app)
    await runner.setup()
    site = web.TCPSite(runner, '0.0.0.0', 8080)
    await site.start()
    logger.info("Health check server started on port 8080")

async def safe_twelvedata_ws(md):
    while True:
        try:
            await md.twelvedata_ws()
        except Exception as e:
            logger.error(f"Twelve Data WebSocket انقطع: {e}")
            await asyncio.sleep(5)

async def main():
    init_db()
    logger.info("قاعدة البيانات جاهزة")

    logger.warning("Claude معطل مؤقتاً – تحليل الأخبار متوقف")

    md = MarketData(SYMBOLS)
    asyncio.create_task(safe_twelvedata_ws(md))

    sig_gen = SignalGenerator(md)
    bot = bot_handlers.TradingBot(TELEGRAM_BOT_TOKEN, sig_gen, md)
    tm = TradeManager(md, bot)

    async def scan_loop():
        while True:
            for sym in SYMBOLS:
                try:
                    signal = await sig_gen.evaluate_symbol(sym)
                    if signal:
                        await tm.open_trade(signal)
                except Exception as e:
                    logger.error(f"Error evaluating {sym}: {e}")
            await asyncio.sleep(30)

    asyncio.create_task(scan_loop())
    asyncio.create_task(tm.monitor_trades())
    asyncio.create_task(run_web_server())

    # تشغيل البوت – الطريقة الجديدة اللي تمنع التعارض
    try:
        logger.info("Starting bot polling...")
        await bot.app.run_polling(drop_pending_updates=True)
    except Exception as e:
        logger.error(f"Bot polling stopped: {e}")

if __name__ == "__main__":
    asyncio.run(main())
