import logging
from datetime import datetime, timedelta
from telegram import ChatPermissions
from telegram.ext import ContextTypes
from models.user import User

logger = logging.getLogger(__name__)

class UserService: 
    @staticmethod
    async def ban_user(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user_id: int, reason: str = None): 
        try:
            await context.bot.ban_chat_member(chat_id, user_id)
            logger.info(f"User {user_id} banned from chat {chat_id}")
            return True, "User banned successfully"
        except Exception as e:
            logger.error(f"Failed to ban user {user_id}: {e}")
            return False, str(e)
    
    @staticmethod
    async def mute_user(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user_id: int, duration: int = None):
        """Mute a user, optionally with a duration in minutes."""
        permissions = ChatPermissions(can_send_messages=False)
        
        try:
            if duration:
                until_date = datetime.now() + timedelta(minutes=duration)
                await context.bot.restrict_chat_member(
                    chat_id, 
                    user_id, 
                    permissions=permissions,
                    until_date=until_date
                )
            else:
                await context.bot.restrict_chat_member(chat_id, user_id, permissions=permissions)
            
            return True, f"User muted{' for ' + str(duration) + ' minutes' if duration else ''}"
        except Exception as e:
            logger.error(f"Failed to mute user {user_id}: {e}")
            return False, str(e)
    
    @staticmethod
    async def unmute_user(context: ContextTypes.DEFAULT_TYPE, chat_id: int, user_id: int):
        """Unmute a user."""
        permissions = ChatPermissions(
            can_send_messages=True,
            can_send_media_messages=True,
            can_send_polls=True,
            can_send_other_messages=True,
            can_add_web_page_previews=True
        )
        
        try:
            await context.bot.restrict_chat_member(chat_id, user_id, permissions=permissions)
            return True, "User unmuted successfully"
        except Exception as e:
            logger.error(f"Failed to unmute user {user_id}: {e}")
            return False, str(e)
    
    @staticmethod
    async def get_muted_users(context: ContextTypes.DEFAULT_TYPE, chat_id: int):
        """Get a list of muted users in the chat."""
        try: 
            # TODO
            # Note: This requires storing muted users in a database
            # For now, return empty list
            return []
        except Exception as e:
            logger.error(f"Failed to get muted users: {e}")
            return []
    
    @staticmethod
    async def remove_user_by_username(context: ContextTypes.DEFAULT_TYPE, chat_id: int, username: str):
        """Remove a user by their username."""
        # This would require finding the user by username
        # For now, just return an error
        return False, "Username lookup not implemented yet"