import logging
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from telegram.constants import ParseMode
from config import Config

logger = logging.getLogger(__name__)

class PrivateHandlers:
    """Handler class for private chat interactions with interactive menus."""
     
    @staticmethod
    async def handle_bot_mention(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle bot mention in groups."""
        try:
            bot_username = context.bot.username
            
            menu_text = (
                f"⚡ **@{bot_username} Admin Commands & Actions** ⚡\n\n"
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
            
            await update.message.reply_text(menu_text, parse_mode=ParseMode.MARKDOWN)
            
        except Exception as e:
            logger.error(f"Error in mention handler: {e}")
     
    @staticmethod
    async def show_main_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show the main interactive menu."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("📚 Commands", callback_data="menu_commands"),
                    InlineKeyboardButton("ℹ️ About", callback_data="menu_about")
                ],
                [
                    InlineKeyboardButton("🔧 Admin Tools", callback_data="menu_admin"),
                    InlineKeyboardButton("📊 Stats", callback_data="menu_stats")
                ],
                [
                    InlineKeyboardButton("❓ Help", callback_data="menu_help"),
                    InlineKeyboardButton("🏠 Home", callback_data="menu_home")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"🤖 **Welcome to the Bot Menu!**\n\n"
                f"Choose an option below to get started:\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"📚 **Commands** - View all available commands\n"
                f"ℹ️ **About** - Learn about this bot\n"
                f"🔧 **Admin Tools** - Group management features\n"
                f"📊 **Stats** - Bot statistics\n"
                f"❓ **Help** - Get assistance"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
            else:
                await update.message.reply_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                
        except Exception as e:
            logger.error(f"Error showing main menu: {e}")
     
    @staticmethod
    async def show_commands_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show commands menu with interactive buttons."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("👤 User Commands", callback_data="menu_user_commands"),
                    InlineKeyboardButton("👑 Admin Commands", callback_data="menu_admin_commands")
                ],
                [
                    InlineKeyboardButton("📝 Moderation", callback_data="menu_moderation"),
                    InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_home")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"📚 **Commands Menu**\n\n"
                f"Select a category to view commands:\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"👤 **User Commands** - Basic commands\n"
                f"👑 **Admin Commands** - Admin-only commands\n"
                f"📝 **Moderation** - Moderation tools"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing commands menu: {e}")
     
    @staticmethod
    async def show_user_commands(update: Update, context: ContextTypes.DEFAULT_TYPE): 
        try:
            keyboard = [
                [
                    InlineKeyboardButton("🚀 /start", callback_data="cmd_start"),
                    InlineKeyboardButton("❓ /help", callback_data="cmd_help")
                ],
                [
                    InlineKeyboardButton("ℹ️ /info", callback_data="cmd_info"),
                    InlineKeyboardButton("🔙 Back to Commands", callback_data="menu_commands")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"👤 **User Commands**\n\n"
                f"Available commands for all users:\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🚀 `/start` - Start the bot\n"
                f"❓ `/help` - Show help menu\n"
                f"ℹ️ `/info` - Bot information\n\n"
                f"*Click a button to use the command*"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing user commands: {e}")
     
    @staticmethod
    async def show_admin_commands(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show admin commands."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("🔨 Ban", callback_data="cmd_ban"),
                    InlineKeyboardButton("🔇 Mute", callback_data="cmd_mute")
                ],
                [
                    InlineKeyboardButton("🔊 Unmute", callback_data="cmd_unmute"),
                    InlineKeyboardButton("📋 Muted List", callback_data="cmd_muted")
                ],
                [
                    InlineKeyboardButton("🗑️ Delete", callback_data="cmd_delete"),
                    InlineKeyboardButton("🧹 Clear", callback_data="cmd_clear")
                ],
                [
                    InlineKeyboardButton("💥 Destroy", callback_data="cmd_destroy"),
                    InlineKeyboardButton("❌ Cancel Destroy", callback_data="cmd_cancel_destroy")
                ],
                [
                    InlineKeyboardButton("🔙 Back to Commands", callback_data="menu_commands")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"👑 **Admin Commands**\n\n"
                f"Admin-only moderation commands:\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔨 `/ban` - Ban a user (reply to message)\n"
                f"🔇 `/mute` - Mute a user (reply to message)\n"
                f"🔊 `/unmute` - Unmute a user\n"
                f"📋 `/muted` - List muted users\n"
                f"🗑️ `/delete` - Delete a message\n"
                f"🧹 `/clear` - Clear messages\n"
                f"💥 `/destroy` - Self-destruct group\n"
                f"❌ `/cancel_destroy` - Cancel destruction\n\n"
                f"*⚠️ These commands only work in groups where I'm admin*"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing admin commands: {e}")
     
    @staticmethod
    async def show_moderation_menu(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show moderation tools menu."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("👥 User Management", callback_data="menu_user_mgmt"),
                    InlineKeyboardButton("📝 Message Control", callback_data="menu_msg_control")
                ],
                [
                    InlineKeyboardButton("🧹 Cleanup Tools", callback_data="menu_cleanup"),
                    InlineKeyboardButton("🔙 Back to Commands", callback_data="menu_commands")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"📝 **Moderation Tools**\n\n"
                f"Select a moderation category:\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"👥 **User Management** - Ban/Mute users\n"
                f"📝 **Message Control** - Delete/Clear messages\n"
                f"🧹 **Cleanup Tools** - Group cleanup"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing moderation menu: {e}")
     
    @staticmethod
    async def show_about(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show about information."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_home")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"ℹ️ **About {Config.BOT_NAME}**\n\n"
                f"🤖 **Name:** {Config.BOT_NAME}\n"
                f"📌 **Version:** {Config.BOT_VERSION}\n"
                f"📅 **Created:** {Config.CREATED_DATE}\n"
                f"👨‍💻 **Developer:** {Config.Developer["name"] },\n phone :{ Config.Developer["phone"]} , \nDM:{Config.Developer["telegram_acc"] }\n\n"
                f"**Features:**\n"
                f"✅ Group Management\n"
                f"✅ User Moderation\n"
                f"✅ Message Control\n"
                f"✅ Auto-Cleanup\n"
                f"✅ Self-Destruction\n\n" 
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing about: {e}")
    
    # ========== ADMIN TOOLS MENU ==========
    @staticmethod
    async def show_admin_tools(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show admin tools menu."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("🔨 Ban User", callback_data="admin_ban"),
                    InlineKeyboardButton("🔇 Mute User", callback_data="admin_mute")
                ],
                [
                    InlineKeyboardButton("📋 List Muted", callback_data="admin_muted"),
                    InlineKeyboardButton("🧹 Clear Chat", callback_data="admin_clear")
                ],
                [
                    InlineKeyboardButton("💥 Destroy Group", callback_data="admin_destroy"),
                    InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_home")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"🔧 **Admin Tools**\n\n"
                f"Quick access to admin functions:\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"🔨 **Ban** - Remove a user from group\n"
                f"🔇 **Mute** - Restrict a user's messages\n"
                f"📋 **Muted** - View muted users list\n"
                f"🧹 **Clear** - Clear chat messages\n"
                f"💥 **Destroy** - Self-destruct group\n\n"
                f"*⚠️ These require admin permissions in the group*"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing admin tools: {e}")
    
    # ========== STATS MENU ==========
    @staticmethod
    async def show_stats(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show bot statistics."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("🔄 Refresh", callback_data="menu_stats"),
                    InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_home")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"📊 **Bot Statistics**\n\n"
                f"📈 **Usage Stats:**\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"👥 **Total Users:** 0\n"
                f"📊 **Active Chats:** 0\n"
                f"⚡ **Commands Executed:** 0\n"
                f"🔄 **Uptime:** Online\n\n"
                f"📌 **Bot Info:**\n"
                f"🤖 Status: 🟢 Online\n"
                f"📱 Platform: Render\n"
                f"🐍 Python: 3.11.11"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing stats: {e}")
    
    # ========== HELP MENU ==========
    @staticmethod
    async def show_help(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show help menu."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("📚 Commands", callback_data="menu_commands"),
                    InlineKeyboardButton("❓ FAQ", callback_data="menu_faq")
                ],
                [
                    InlineKeyboardButton("💬 Support", callback_data="menu_support"),
                    InlineKeyboardButton("🔙 Back to Menu", callback_data="menu_home")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"❓ **Help Center**\n\n"
                f"How can I help you today?\n"
                f"━━━━━━━━━━━━━━━━━━━━━\n"
                f"📚 **Commands** - View all commands\n"
                f"❓ **FAQ** - Frequently asked questions\n"
                f"💬 **Support** - Get assistance"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing help: {e}")
    
    # ========== FAQ ==========
    @staticmethod
    async def show_faq(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Show FAQ."""
        try:
            keyboard = [
                [
                    InlineKeyboardButton("❓ How to use?", callback_data="faq_howto"),
                    InlineKeyboardButton("🔧 Need admin?", callback_data="faq_admin")
                ],
                [
                    InlineKeyboardButton("🔙 Back to Help", callback_data="menu_help")
                ]
            ]
            
            reply_markup = InlineKeyboardMarkup(keyboard)
            
            text = (
                f"❓ **Frequently Asked Questions**\n\n"
                f"**Q: How to use the bot?**\n"
                f"A: Add me to a group and make me admin!\n\n"
                f"**Q: Why do I need to make you admin?**\n"
                f"A: To use moderation commands like ban/mute\n\n"
                f"**Q: Can I use commands in private?**\n"
                f"A: Yes! Use /help to see available commands\n\n"
                f"**Q: Is the bot free?**\n"
                f"A: Yes, it's completely free!"
            )
            
            if update.callback_query:
                await update.callback_query.message.edit_text(
                    text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
                await update.callback_query.answer()
                
        except Exception as e:
            logger.error(f"Error showing FAQ: {e}")
    
    # ========== HANDLE CALLBACK QUERIES ==========
    @staticmethod
    async def handle_callback_query(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle all callback queries from inline keyboards."""
        query = update.callback_query
        data = query.data
        
        # Map callback data to functions
        menu_map = {
            # Main menu
            "menu_home": PrivateHandlers.show_main_menu,
            "menu_commands": PrivateHandlers.show_commands_menu,
            "menu_about": PrivateHandlers.show_about,
            "menu_admin": PrivateHandlers.show_admin_tools,
            "menu_stats": PrivateHandlers.show_stats,
            "menu_help": PrivateHandlers.show_help,
            
            # Commands submenus
            "menu_user_commands": PrivateHandlers.show_user_commands,
            "menu_admin_commands": PrivateHandlers.show_admin_commands,
            "menu_moderation": PrivateHandlers.show_moderation_menu,
            
            # FAQ
            "menu_faq": PrivateHandlers.show_faq,
            
            # Command actions (simple responses)
            "cmd_start": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/start"),
            "cmd_help": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/help"),
            "cmd_info": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/info"),
            "cmd_ban": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/ban"),
            "cmd_mute": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/mute"),
            "cmd_unmute": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/unmute"),
            "cmd_muted": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/muted"),
            "cmd_delete": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/delete"),
            "cmd_clear": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/clear"),
            "cmd_destroy": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/destroy"),
            "cmd_cancel_destroy": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/cancel_destroy"),
            
            # Admin tools
            "admin_ban": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/ban"),
            "admin_mute": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/mute"),
            "admin_muted": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/muted"),
            "admin_clear": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/clear"),
            "admin_destroy": lambda u, c: PrivateHandlers._handle_command_action(u, c, "/destroy"),
        }
        
        # Execute the mapped function or show a default response
        if data in menu_map:
            await menu_map[data](update, context)
        else:
            await query.answer("🔧 Feature coming soon!")
            await query.message.reply_text(
                "🚧 This feature is under development. Try the main menu!",
                reply_markup=InlineKeyboardMarkup([
                    [InlineKeyboardButton("🏠 Go to Menu", callback_data="menu_home")]
                ])
            )
    
    @staticmethod
    async def _handle_command_action(update: Update, context: ContextTypes.DEFAULT_TYPE, command: str):
        """Handle command button actions."""
        query = update.callback_query
        await query.answer(f"📝 Type {command} in the chat to use this command")
        await query.message.reply_text(
            f"📝 **Usage:** Type `{command}` in the chat\n\n"
            f"💡 *Tip:* Use this command in a group where I'm admin!",
            parse_mode=ParseMode.MARKDOWN
        )
    
    # ========== PRIVATE MESSAGE HANDLER ==========
    @staticmethod
    async def handle_private_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
        """Handle private messages sent directly to the bot."""
        try:
            user = update.effective_user
            
            # Check if user has interacted before
            if not context.user_data.get('has_interacted'):
                context.user_data['has_interacted'] = True
                
                # Send welcome message with menu
                welcome_text = (
                    f"👋 Hello {user.first_name}!\n\n"
                    f"Welcome to the bot! I'm a group management assistant.\n"
                    f"Use the buttons below to navigate:"
                )
                
                keyboard = [
                    [
                        InlineKeyboardButton("🏠 Main Menu", callback_data="menu_home"),
                        InlineKeyboardButton("📚 Commands", callback_data="menu_commands")
                    ]
                ]
                
                reply_markup = InlineKeyboardMarkup(keyboard)
                await update.message.reply_text(
                    welcome_text, 
                    reply_markup=reply_markup, 
                    parse_mode=ParseMode.MARKDOWN
                )
            else:
                # Regular response with menu
                await PrivateHandlers.show_main_menu(update, context)
                
        except Exception as e:
            logger.error(f"Error in private message handler: {e}")