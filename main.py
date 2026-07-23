import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes

# Load environment variables from .env file
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets each new member who joins the group."""
    for new_member in update.message.new_chat_members: 
        if new_member.id == context.bot.id:
            continue 
        first_name = new_member.first_name
        welcome_text = f"Welcome to the group, {first_name}! 👋\nGlad to have you here!"
         
        await update.message.reply_text(welcome_text)

if __name__ == '__main__': 
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is missing! Make sure it is set in your .env file or environment.")

    app = ApplicationBuilder().token(token).build()
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))

    print("Greeting bot running...")
    app.run_polling()