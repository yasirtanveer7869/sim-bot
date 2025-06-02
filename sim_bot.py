from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
import requests

BOT_TOKEN = '7788507752:AAF6CgujSlYKUnC2NbabxH8XuXyPiDAJhVw'

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Welcome! Send /sim <number> to get details.\nExample: /sim 03020916003")

async def sim_details(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) != 1:
        await update.message.reply_text("Please provide a valid number. Example: /sim 03020916003")
        return

    number = context.args[0]
    url = f"https://freshsimdetails.com/wp-json/sim-search/v1/fetch-data?number={number}"

    try:
        response = requests.get(url)
        data = response.json()
        
        if data.get("data"):
            result = data["data"]
            # You can format this based on the API structure
            msg = "\n".join([f"{key}: {value}" for key, value in result.items()])
            await update.message.reply_text(msg)
        else:
            await update.message.reply_text("No data found or invalid number.")
    except Exception as e:
        await update.message.reply_text(f"Error: {str(e)}")

if __name__ == '__main__':
    app = ApplicationBuilder().token(BOT_TOKEN).build()

    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("sim", sim_details))

    print("Bot is running...")
    app.run_polling()
