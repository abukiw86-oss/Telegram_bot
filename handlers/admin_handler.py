from telegram import Update
from telegram.ext import ContextTypes
from utils.decorators import admin_required, get_target_user
from services.user_service import UserService
from services.admin_service import AdminService
from services.cleanup_service import CleanupService

class AdminHandlers: 
    @staticmethod
    @admin_required
    async def delete_message(update: Update, context: ContextTypes.DEFAULT_TYPE): 
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Reply to the message you want to delete.")
            return
        
        message_id = update.message.reply_to_message.message_id
        chat_id = update.effective_chat.id
        
        success, message = await AdminService.delete_message(context, chat_id, message_id)
        await update.message.reply_text(f"{'✅' if success else '❌'} {message}")
    
    @staticmethod
    @admin_required
    async def unmute_user(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Unmute a user."""
        if not update.message.reply_to_message:
            await update.message.reply_text("⚠️ Reply to the muted user's message with `/unmute`.")
            return
        
        target_user = update.message.reply_to_message.from_user
        chat_id = update.effective_chat.id
        
        success, message = await UserService.unmute_user(context, chat_id, target_user.id)
        await update.message.reply_text(f"{'✅' if success else '❌'} {message}")
    
    @staticmethod
    @admin_required
    async def list_muted_users(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """List all muted users."""
        chat_id = update.effective_chat.id
        muted_users = await UserService.get_muted_users(context, chat_id)
        
        if not muted_users:
            await update.message.reply_text("📋 No muted users found.")
            return
        
        response = "📋 **Muted Users:**\n\n"
        for user in muted_users:
            response += f"• {user.first_name}"
            if user.username:
                response += f" (@{user.username})"
            if user.muted_until:
                response += f" - until {user.muted_until}"
            response += "\n"
        
        await update.message.reply_text(response, parse_mode="Markdown")
    
    @staticmethod
    @admin_required
    async def clear_messages(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Clear messages with optional count or timer."""
        chat_id = update.effective_chat.id
         
        
        if context.args:
            if context.args[0].lower() == 'now':
                success, message = await CleanupService.clear_messages(context, chat_id)
                await update.message.reply_text(f"{'✅' if success else '❌'} {message}")
                return
             
            try:
                if 'm' in context.args[0]:  # Minutes
                    minutes = int(context.args[0].replace('m', '')) 
                    pass
                else:  
                    count = int(context.args[0])
                    success, message = await CleanupService.clear_messages(context, chat_id, count=count)
                    await update.message.reply_text(f"{'✅' if success else '❌'} {message}")
            except ValueError:
                await update.message.reply_text("⚠️ Invalid format. Use `/clear <count>` or `/clear now`")
        else:
            await update.message.reply_text("⚠️ Use `/clear <count>` or `/clear now`")
    
    @staticmethod
    @admin_required
    async def schedule_destruction(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Schedule group self-destruction."""
        chat_id = update.effective_chat.id
        admin_id = update.effective_user.id 
        
        timer_days = None
        timer_hours = None
        timer_minutes = None
        
        if context.args:
            arg = context.args[0]
            if 'd' in arg:
                timer_days = int(arg.replace('d', ''))
            elif 'h' in arg:
                timer_hours = int(arg.replace('h', ''))
            elif 'm' in arg:
                timer_minutes = int(arg.replace('m', ''))
            else:
                await update.message.reply_text("⚠️ Use format: `/destroy 30d` (days), `/destroy 12h` (hours), or `/destroy 45m` (minutes)")
                return
        
        success, message = await CleanupService.schedule_group_destruction(
            context, chat_id, admin_id, 
            timer_days=timer_days, 
            timer_hours=timer_hours, 
            timer_minutes=timer_minutes
        )
        await update.message.reply_text(f"{'✅' if success else '❌'} {message}")
    
    @staticmethod
    @admin_required
    async def cancel_destruction(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Cancel scheduled group destruction."""
        chat_id = update.effective_chat.id
        admin_id = update.effective_user.id
        
        success, message = await CleanupService.cancel_destruction(context, chat_id, admin_id)
        await update.message.reply_text(f"{'✅' if success else '❌'} {message}")