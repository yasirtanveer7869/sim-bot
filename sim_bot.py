import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes

BOT_TOKEN = os.getenv("BOT_TOKEN")  # Get token from Railway environment variable

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("👋 Welcome! Send /sim <number> to get SIM details.\n\nExample:\n/sim 03020916003")

async def sim(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("❌ Please provide a valid number.\nExample: /sim 03020916003")
        return

    number = context.args[0]
    api_url = f"https://freshsimdetails.com/wp-json/sim-search/v1/fetch-data?number={number}"

    try:
        response = requests.get(api_url)
        data = response.json()

        if data.get("data"):
            result = data["data"]
            message = "\n".join([f"{key}: {value}" for key, value in result.items()])
            await update.message.reply_text(f"📱 SIM Details:\n{message}")
        else:
            await update.message.reply_text("⚠️ No data found or number is invalid.")
    except Exception as e:
        await update.message.reply_text(f"🚫 Error: {str(e)}")

if __name__ == "__main__":
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sim", sim))

    print("🤖 Bot is running...")
    app.run_polling()
