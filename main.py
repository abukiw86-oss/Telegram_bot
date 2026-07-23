import os
import sys
import asyncio
import logging
from flask import Flask
from threading import Thread 
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes, CallbackQueryHandler
from config import Config
from handlers.admin_handler import AdminHandlers
from handlers.user_handler import UserHandlers
from handlers.private_handler import PrivateHandlers
 
import warnings
warnings.filterwarnings("ignore", category=UserWarning, module='werkzeug')

logger = logging.getLogger(__name__)
 
web_app = Flask(__name__)

@web_app.route('/')
def health_check():
    return "Bot is running!", 200

@web_app.route('/health')
def health():
    return {"status": "healthy"}, 200

def run_web_server():
    """Run a simple web server to keep Render happy."""
    try:
        port = int(os.environ.get('PORT', 10000)) 
        web_app.run(host='0.0.0.0', port=port, debug=False, use_reloader=False)
    except Exception as e:
        logger.error(f"Web server error: {e}")

class TelegramBot: 
    def __init__(self):
        Config.setup_logging()
        
        try:
            Config.validate()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            sys.exit(1)
        
        self.token = Config.BOT_TOKEN
        self.application = None
        self._setup_web_server()
        self._setup_handlers()
    
    def _setup_web_server(self): 
        web_thread = Thread(target=run_web_server, daemon=True)
        web_thread.start()
        logger.info(f"🌐 Web server started on port {os.environ.get('PORT', 10000)}")
    
    def _setup_handlers(self): 
        try:
            self.application = ApplicationBuilder().token(self.token).build()
             
            self.application.add_handler(CommandHandler("start", PrivateHandlers.show_main_menu))
            self.application.add_handler(CommandHandler("help", PrivateHandlers.show_help))
            self.application.add_handler(CommandHandler("info", PrivateHandlers.show_about))
             
            self.application.add_handler(
                CallbackQueryHandler(PrivateHandlers.handle_callback_query)
            ) 
            self.application.add_handler(
                MessageHandler(
                    filters.ChatType.PRIVATE & filters.TEXT & ~filters.COMMAND,
                    PrivateHandlers.handle_private_message
                )
            ) 

            self.application.add_handler(CommandHandler("ban", UserHandlers.ban_user))
            self.application.add_handler(CommandHandler("remove", UserHandlers.ban_user))
            self.application.add_handler(CommandHandler("mute", UserHandlers.mute_user))
            self.application.add_handler(CommandHandler("unmute", AdminHandlers.unmute_user))
            self.application.add_handler(CommandHandler("muted", AdminHandlers.list_muted_users))
            self.application.add_handler(CommandHandler("remove_user", UserHandlers.remove_user_by_username))
            self.application.add_handler(CommandHandler("delete", AdminHandlers.delete_message))
            self.application.add_handler(CommandHandler("clear", AdminHandlers.clear_messages))
            self.application.add_handler(CommandHandler("destroy", AdminHandlers.schedule_destruction))
            self.application.add_handler(CommandHandler("cancel_destroy", AdminHandlers.cancel_destruction))
            self.application.add_handler(CommandHandler("purge", AdminHandlers.delete_message))
             
            self.application.add_handler(
                MessageHandler(
                    filters.StatusUpdate.NEW_CHAT_MEMBERS, 
                    UserHandlers.greet_new_member
                )
            )
            self.application.add_handler(
                MessageHandler(
                    filters.StatusUpdate.LEFT_CHAT_MEMBER, 
                    UserHandlers.farewell_member
                )
            )
             
            self.application.add_handler(
                MessageHandler(
                    (filters.Entity("mention") | filters.Entity("text_mention")) & filters.ChatType.GROUPS,
                    PrivateHandlers.handle_bot_mention
                )
            )
            
            logger.info("✅ All handlers registered successfully")
            
        except Exception as e:
            logger.error(f"Failed to setup handlers: {e}")
            raise
    
    async def run_async(self): 
        try:
            logger.info("🚀 Starting Telegram Bot...")
            print("🤖 Admin & Greeting bot running on Render...")
            
            await self.application.initialize()
            await self.application.start()
            await self.application.updater.start_polling(
                drop_pending_updates=True,
                allowed_updates=['message', 'chat_member', 'callback_query', 'my_chat_member']
            )
             
            while True:
                await asyncio.sleep(3600)
                
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Error while running bot: {e}")
            raise
        finally:
            await self._cleanup()
    
    async def _cleanup(self): 
        try:
            if self.application:
                await self.application.updater.stop()
                await self.application.stop()
                await self.application.shutdown()
                logger.info("✅ Bot shutdown complete")
        except Exception as e:
            logger.error(f"Error during shutdown: {e}")
    
    def run(self): 
        try:
            asyncio.run(self.run_async())
        except KeyboardInterrupt:
            logger.info("Bot stopped by user")
        except Exception as e:
            logger.error(f"Fatal error: {e}")
            sys.exit(1)

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()