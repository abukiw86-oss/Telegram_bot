import os
import sys
import asyncio
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from config import Config
from handlers.admin_handler import AdminHandlers
from handlers.user_handler import UserHandlers

# Import for web server
from flask import Flask
from threading import Thread

logger = logging.getLogger(__name__)

# Create Flask app for health checks
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "Bot is running!", 200

@web_app.route('/health')
def health():
    return {"status": "healthy"}, 200

def run_web_server():
    """Run a simple web server to keep Render happy."""
    port = int(os.environ.get('PORT', 10000))
    web_app.run(host='0.0.0.0', port=port)

async def handle_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
    """Handle bot mention to show menu."""
    try:
        bot_username = context.bot.username
        
        menu_text = (
            f"⚡ **{bot_username} Admin Commands & Actions** ⚡\n\n"
            f"👑 *Admin-Only Commands:*\n"
            f"• `/ban` (or reply with `/ban`) - Remove member\n"
            f"• `/unmute` - Unmute a member (reply to their message)\n"
            f"• `/muted` - List all muted users\n"
            f"• `/delete` or `/purge` - Delete a message (reply to it)\n"
            f"• `/clear <count|now>` - Clear messages\n"
            f"• `/remove_user @username` - Remove user by username\n"
            f"• `/destroy <time>` - Self-destruct group (30d/12h/45m)\n"
            f"• `/cancel_destroy` - Cancel scheduled destruction\n\n"
            f"ℹ️ *Note:* Non-admins cannot execute moderation actions!"
        )
        
        await update.message.reply_text(menu_text, parse_mode="Markdown")
    except Exception as e:
        logger.error(f"Error in mention handler: {e}")

async def main(): 
    Config.setup_logging()
    
    try:
        Config.validate()
    except ValueError as e:
        logger.error(f"Configuration error: {e}")
        sys.exit(1)
    
    # Start web server in a separate thread
    web_thread = Thread(target=run_web_server, daemon=True)
    web_thread.start()
    logger.info(f"🌐 Web server started on port {os.environ.get('PORT', 10000)}")
     
    application = ApplicationBuilder().token(Config.BOT_TOKEN).build()
     
    application.add_handler(CommandHandler("ban", UserHandlers.ban_user))
    application.add_handler(CommandHandler("remove", UserHandlers.ban_user))
    application.add_handler(CommandHandler("mute", UserHandlers.mute_user))
    application.add_handler(CommandHandler("unmute", AdminHandlers.unmute_user))
    application.add_handler(CommandHandler("muted", AdminHandlers.list_muted_users))
    application.add_handler(CommandHandler("remove_user", UserHandlers.remove_user_by_username))
     
    application.add_handler(CommandHandler("delete", AdminHandlers.delete_message))
    application.add_handler(CommandHandler("clear", AdminHandlers.clear_messages))
    application.add_handler(CommandHandler("destroy", AdminHandlers.schedule_destruction))
    application.add_handler(CommandHandler("cancel_destroy", AdminHandlers.cancel_destruction))
    application.add_handler(CommandHandler("purge", AdminHandlers.delete_message))
     
    application.add_handler(
        MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, UserHandlers.greet_new_member)
    )
    application.add_handler(
        MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, UserHandlers.farewell_member)
    )
     
    application.add_handler(
        MessageHandler(filters.Entity("mention") | filters.Entity("text_mention"), handle_mention)
    )
    
    logger.info("✅ All handlers registered successfully")
    logger.info("🚀 Starting Telegram Bot...")
    print("🤖 Admin & Greeting bot running on Render...")
     
    try: 
        await application.initialize()
        await application.start()
        await application.updater.start_polling(
            drop_pending_updates=True,
            allowed_updates=['message', 'chat_member']
        )
         
        while True:
            await asyncio.sleep(3600)  
            
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Error while running bot: {e}")
        raise
    finally:
        try:
            await application.updater.stop()
            await application.stop()
            await application.shutdown()
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")

if __name__ == '__main__':
    try: 
        asyncio.run(main())
    except KeyboardInterrupt:
        logger.info("Bot stopped by user")
    except Exception as e:
        logger.error(f"Fatal error: {e}")
        sys.exit(1)