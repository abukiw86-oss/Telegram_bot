import os
import logging
from dotenv import load_dotenv
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, filters, ContextTypes
 
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)

async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Greets each new member who joins the group."""
    for new_member in update.message.new_chat_members:  
        if new_member.id == context.bot.id:
            welcome_text = f"I Came To you On this Group ! 👋\nHA HA HA 👋"  #we added the group name 
            
        first_name = new_member.first_name
        welcome_text = f"Welcome to the group, {first_name}! 👋\nGlad to have you here!"
         
        await update.message.reply_text(welcome_text)

async def farewell_left_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Sends a dramatic pity/farewell message when someone leaves."""
    left_member = update.message.left_chat_member 
    if left_member.id == context.bot.id:
        return
        
    first_name = left_member.first_name
     
    farewell_text = (
        f"Oh no, {first_name} left us... 💔😢\n\n"
        f"Was it something we said? We'll miss you!\n"
        f"If you ever change your mind, the door is always open. Come back soon! 🥺"
    )
    
    await update.message.reply_text(farewell_text)

if __name__ == '__main__': 
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is missing! Make sure it is set in your .env file or environment.")

    app = ApplicationBuilder().token(token).build()
 
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
     
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, farewell_left_member))

    print("Greeting & Farewell bot running...")
    app.run_polling()