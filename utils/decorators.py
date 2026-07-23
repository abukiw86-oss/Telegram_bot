from functools import wraps
from telegram import Update
from telegram.ext import ContextTypes

async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['administrator', 'creator']

def admin_required(func):
    """Decorator to check if user is admin before executing command."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        if not await is_user_admin(update, context):
            await update.message.reply_text("❌ Permission Denied: Only admins can perform this action.")
            return
        return await func(update, context, *args, **kwargs)
    return wrapper

def get_target_user(func):
    """Decorator to extract target user from reply or mention."""
    @wraps(func)
    async def wrapper(update: Update, context: ContextTypes.DEFAULT_TYPE, *args, **kwargs):
        target_user = None 
        if update.message.reply_to_message:
            target_user = update.message.reply_to_message.from_user 
            
        if not target_user and context.args:
            username = context.args[0].replace('@', '')
            try:
                # TODO
                # Try to get user by username (might need additional logic)
                pass
            except:
                pass
        
        if not target_user:
            await update.message.reply_text("⚠️ Please reply to the user's message or provide a username.")
            return
        
        return await func(update, context, target_user, *args, **kwargs)
    return wrapper