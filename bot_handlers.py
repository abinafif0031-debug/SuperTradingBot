from telegram import Update, ReplyKeyboardMarkup
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes

class TradingBot:
    def __init__(self, token, signal_generator, market_data, trade_manager):
        self.app = Application.builder().token(token).build()
        self.signal_gen = signal_generator
        self.md = market_data
        self.tm = trade_manager
        self.paused = False

        # لوحة المفاتيح الدائمة
        self.keyboard = ReplyKeyboardMarkup(
            [
                ["📊 تحليل سهم", "📈 الصفقات المفتوحة"],
                ["📉 إحصائيات اليوم", "⏸️ إيقاف الإشارات"],
                ["▶️ استئناف الإشارات"]
            ],
            resize_keyboard=True,
            persistent=True
        )

        # تسجيل الأوامر
        self.app.add_handler(CommandHandler("start", self.start))
        self.app.add_handler(CommandHandler("menu", self.show_menu))
        self.app.add_handler(CommandHandler("stats", self.daily_stats))
        self.app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, self.handle_message))

    async def start(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text(
            "🦁 البوت الوحش جاهز للانقضاض\nاختر من الأزرار أدناه:",
            reply_markup=self.keyboard
        )

    async def show_menu(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        await update.message.reply_text("اختر العملية:", reply_markup=self.keyboard)

    async def daily_stats(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        # عرض إحصائيات اليوم
        # يمكن جلبها من trade_manager أو قاعدة البيانات
        # حالياً نعرض قيم ثابتة للتجربة
        stats_text = (
            "📊 إحصائيات اليوم\n"
            "عدد الصفقات: 0\n"
            "الصفقات الرابحة: 0\n"
            "الخاسرة: 0\n"
            "الربح/الخسارة: $0.00"
        )
        await update.message.reply_text(stats_text, reply_markup=self.keyboard)

    async def handle_message(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
        text = update.message.text.strip()
        chat_id = update.effective_chat.id

        if text == "📊 تحليل سهم":
            await update.message.reply_text("أرسل رمز السهم (مثل AAPL):", reply_markup=self.keyboard)
            # يمكن الانتظار للرسالة التالية (نستخدم context.user_data)
            context.user_data['expecting_symbol'] = True
            return

        if text == "📈 الصفقات المفتوحة":
            trades = self.tm.active_trades
            if not trades:
                msg = "لا توجد صفقات مفتوحة حالياً."
            else:
                msg = "📈 الصفقات المفتوحة:\n"
                for t in trades:
                    msg += f"{t['symbol']} | دخول: {t['entry']:.2f} | هدف1: {t['target1']:.2f}\n"
            await update.message.reply_text(msg, reply_markup=self.keyboard)
            return

        if text == "📉 إحصائيات اليوم":
            await self.daily_stats(update, context)
            return

        if text == "⏸️ إيقاف الإشارات":
            self.paused = True
            await update.message.reply_text("⏸️ تم إيقاف إرسال الإشارات الجديدة.", reply_markup=self.keyboard)
            return

        if text == "▶️ استئناف الإشارات":
            self.paused = False
            await update.message.reply_text("▶️ تم استئناف الإشارات.", reply_markup=self.keyboard)
            return

        # إذا كان المستخدم أرسل رمز سهم بعد طلب التحليل
        if context.user_data.get('expecting_symbol'):
            symbol = text.upper().strip()
            context.user_data['expecting_symbol'] = False
            # تحليل سريع عبر signal_generator (اختياري)
            try:
                signal = await self.signal_gen.evaluate_symbol(symbol)
                if signal:
                    msg = f"📊 {symbol}\n"
                    msg += f"سعر الدخول: {signal['entry']:.2f}\n"
                    msg += f"وقف: {signal['stop']:.2f}\n"
                    msg += f"هدف1: {signal['target1']:.2f}\n"
                    msg += f"هدف2: {signal['target2']:.2f}\n"
                    msg += f"النوع: {signal['type']}\n"
                    msg += f"الثقة: {signal['confidence']}/10"
                else:
                    msg = f"⚠️ {symbol}: لا توجد إشارة حالياً."
            except Exception as e:
                msg = f"خطأ في التحليل: {e}"
            await update.message.reply_text(msg, reply_markup=self.keyboard)
            return

        # أي رسالة أخرى
        await update.message.reply_text("استخدم الأزرار أو أرسل /menu", reply_markup=self.keyboard)

    async def send_message(self, chat_id, text):
        await self.app.bot.send_message(chat_id=chat_id, text=text)
