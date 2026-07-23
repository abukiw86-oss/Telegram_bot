import os
import logging
from dotenv import load_dotenv
from telegram import Update , ChatAdministratorRights , ChatPermissions
from telegram.ext import ApplicationBuilder, MessageHandler, CommandHandler, filters, ContextTypes
 
load_dotenv()

logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
 
async def is_user_admin(update: Update, context: ContextTypes.DEFAULT_TYPE) -> bool:
    chat_id = update.effective_chat.id
    user_id = update.effective_user.id
    
    member = await context.bot.get_chat_member(chat_id, user_id)
    return member.status in ['administrator', 'creator']


async def greet_new_member(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    for new_member in update.message.new_chat_members: 
        if new_member.id == context.bot.id:
            continue 
            
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


async def handle_bot_mention(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    bot_username = context.bot.username
    
    menu_text = (
        f"⚡ **{bot_username} Admin Commands & Actions** ⚡\n\n"
        f"👑 *Admin-Only Commands:*\n"
        f"• `/ban` (or reply to a user with `/ban`) - Remove member from group\n"
        f"• `/unban` `<user_id>` - Unban a user\n"
        f"• `/mute` - Mute a member (reply to their message)\n"
        f"• `/unmute` - Unmute a member\n"
        f"• `/pin` - Pin a message (reply to message)\n"
        f"• `/purge` - Delete referenced message\n\n"
        f"ℹ️ *Note:* Non-admins cannot execute moderation actions!"
    )
    
    await update.message.reply_text(menu_text, parse_mode="Markdown")


async def ban_user(update: Update, context: ContextTypes.DEFAULT_TYPE):  
    if not await is_user_admin(update, context):
        await update.message.reply_text("❌ Permission Denied: Only admins can perform this action.")
        return
 
    target_user = None
    if update.message.reply_to_message:
        target_user = update.message.reply_to_message.from_user
    
    if not target_user:
        await update.message.reply_text("⚠️ Please reply to the user's message you want to ban with `/ban`.")
        return
 
    target_member = await context.bot.get_chat_member(update.effective_chat.id, target_user.id)
    if target_member.status in ['administrator', 'creator']:
        await update.message.reply_text("⚠️ You cannot ban another admin!")
        return
 
    try:
        await context.bot.ban_chat_member(update.effective_chat.id, target_user.id)
        await update.message.reply_text(f"🚫 {target_user.first_name} (@{target_user.username}) has been removed from the group.")
    except Exception as e:
        await update.message.reply_text(f"Failed to remove user: {str(e)}")


async def mute_user(update: Update, context: ContextTypes.DEFAULT_TYPE): 
    if not await is_user_admin(update, context):
        await update.message.reply_text("❌ Permission Denied: Only admins can perform this action.")
        return

    if not update.message.reply_to_message:
        await update.message.reply_text("⚠️ Reply to the user's message with `/mute` to mute them.")
        return

    target_user = update.message.reply_to_message.from_user
    
    from telegram import ChatPermissions
    no_permissions = ChatPermissions(can_send_messages=False)

    try:
        await context.bot.restrict_chat_member(update.effective_chat.id, target_user.id, permissions=no_permissions)
        await update.message.reply_text(f"🤐 {target_user.first_name} has been muted.")
    except Exception as e:
        await update.message.reply_text(f"Failed to mute user: {str(e)}")
        
if __name__ == '__main__': 
    token = os.environ.get("BOT_TOKEN")

    if not token:
        raise ValueError("BOT_TOKEN is missing! Make sure it is set in your .env file or environment.")

    app = ApplicationBuilder().token(token).build()
 
    app.add_handler(MessageHandler(filters.StatusUpdate.NEW_CHAT_MEMBERS, greet_new_member))
    app.add_handler(MessageHandler(filters.StatusUpdate.LEFT_CHAT_MEMBER, farewell_left_member))
     
    app.add_handler(MessageHandler(filters.Entity("mention") | filters.Entity("text_mention"), handle_bot_mention))
 
    app.add_handler(CommandHandler("ban", ban_user))
    app.add_handler(CommandHandler("remove", ban_user))
    app.add_handler(CommandHandler("mute", mute_user)) 
    print("Admin & Greeting bot running...")
    app.run_polling()