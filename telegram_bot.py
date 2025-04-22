from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes, MessageHandler, filters
from agent_controller import handle_location_query

from dotenv import load_dotenv
import os

load_dotenv()

TELEGRAM_BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Hi there! Enter the location you'd like to explore: ")

async def location_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    location = update.message.text
    response = await handle_location_query(location)
    await update.message.reply_text(response[:4000])


app = ApplicationBuilder().token(TELEGRAM_BOT_TOKEN).build()
app.add_handler(CommandHandler("start", start))
app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, location_handler))

app.run_polling()