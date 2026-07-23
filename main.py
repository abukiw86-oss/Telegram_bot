import os
import sys
import logging
from telegram import Update
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
from config import Config
from handlers.admin_handler import AdminHandlers
from handlers.user_handler import UserHandlers

logger = logging.getLogger(__name__)

class TelegramBot:
    """Main bot class."""
    
    def __init__(self):
        Config.setup_logging()
        try:
            Config.validate()
        except ValueError as e:
            logger.error(f"Configuration error: {e}")
            sys.exit(1)
            
        self.token = Config.BOT_TOKEN
        self.application = None
        self._setup_handlers()
    
    def _setup_handlers(self):
        """Setup all command and message handlers."""
        try:
            self.application = ApplicationBuilder().token(self.token).build()
            
            # User-related commands
            self.application.add_handler(CommandHandler("ban", UserHandlers.ban_user))
            self.application.add_handler(CommandHandler("remove", UserHandlers.ban_user))
            self.application.add_handler(CommandHandler("mute", UserHandlers.mute_user))
            self.application.add_handler(CommandHandler("unmute", AdminHandlers.unmute_user))
            self.application.add_handler(CommandHandler("muted", AdminHandlers.list_muted_users))
            self.application.add_handler(CommandHandler("remove_user", UserHandlers.remove_user_by_username))
            
            # Admin commands
            self.application.add_handler(CommandHandler("delete", AdminHandlers.delete_message))
            self.application.add_handler(CommandHandler("clear", AdminHandlers.clear_messages))
            self.application.add_handler(CommandHandler("destroy", AdminHandlers.schedule_destruction))
            self.application.add_handler(CommandHandler("cancel_destroy", AdminHandlers.cancel_destruction))
            self.application.add_handler(CommandHandler("purge", AdminHandlers.delete_message))
            
            # Status updates
            self.application.add_handler(
                MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, UserHandlers.greet_new_member)
            )
            self.application.add_handler(
                MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, UserHandlers.farewell_member)
            )
            
            # Mention handler
            self.application.add_handler(
                MessageHandler(filters.Entity("mention") | filters.Entity("text_mention"), self._handle_mention)
            )
            
            logger.info("✅ All handlers registered successfully")
        except Exception as e:
            logger.error(f"Failed to setup handlers: {e}")
            raise
    
    async def _handle_mention(self, update: Update, context: ContextTypes.DEFAULT_TYPE):
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
    
    def run(self):
        """Start the bot with proper error handling."""
        try:
            logger.info("🚀 Starting Telegram Bot...")
            print("🤖 Admin & Greeting bot running on Render...")
            
            # Start the bot with polling
            self.application.run_polling(
                drop_pending_updates=True,  # Ignore updates while bot was offline
                allowed_updates=['message', 'chat_member']  # Only listen to these update types
            )
        except Exception as e:
            logger.error(f"Fatal error while running bot: {e}")
            sys.exit(1)

if __name__ == '__main__':
    bot = TelegramBot()
    bot.run()