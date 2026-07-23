from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_required
from services.user_service import UserService

class UserHandlers:
    """Handler class for user-related commands."""
    
    @staticmethod
    @admin_required
    async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Ban a user (reply to their message)."""
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Reply to the user's message with `/ban`.")
            return
        
        target_user = update.message.reply_to_message.from_user
        chat_id = update.effective_chat.id
        
        # Check if target is admin
        target_member = await context.bot.get_chat_member(chat_id, target_user.id)
        if target_member.status in ['administrator', 'creator']:
            await update.message.reply_text("⚠️ You cannot ban another admin!")
            return
        
        success, message = await UserService.ban_user(context, chat_id, target_user.id)
        await update.message.reply_text(f"{'✅' if success else '❌'} {message}")
    
    @staticmethod
    @admin_required
    async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Mute a user (reply to their message)."""
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Reply to the user's message with `/mute`.")
            return
        
        target_user = update.message.reply_to_message.from_user
        chat_id = update.effective_chat.id
        
        # Parse optional duration
        duration = None
        if context.args:
            try:
                duration = int(context.args[0])
            except ValueError:
                await update.message.reply_text("⚠️ Invalid duration. Use `/mute <minutes>`")
                return
        
        success, message = await UserService.mute_user(context, chat_id, target_user.id, duration)
        await update.message.reply_text(f"{'✅' if success else '❌'} {message}")
    
    @staticmethod
    @admin_required
    async def remove_user_by_username(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Remove a user by their username."""
        if not context.args:
            await update.message.reply_text("⚠️ Provide username: `/remove @username`")
            return
        
        username = context.args[0].replace('@', '')
        chat_id = update.effective_chat.id
        
        success, message = await UserService.remove_user_by_username(context, chat_id, username)
        await update.message.reply_text(f"{'✅' if success else '❌'} {message}")
    
    @staticmethod
    async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Greet new members."""
        for new_member in update.message.new_chat_members:
            if new_member.id == context.bot.id:
                continue
            
            first_name = new_member.first_name
            welcome_text = f"Welcome to the group, {first_name}! 👋\nGlad to have you here!"
            await update.message.reply_text(welcome_text)
    
    @staticmethod
    async def farewell_member(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Farewell message when someone leaves."""
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