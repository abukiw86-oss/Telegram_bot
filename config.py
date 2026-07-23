import os
from dotenv import load_dotenv
import logging
import sys
 
load_dotenv()

class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    DEFAULT_EXPIRY_YEARS = int(os.environ.get("DEFAULT_EXPIRY_YEARS", 10))
    ENVIRONMENT = os.environ.get("ENVIRONMENT", "production")

    BOT_NAME = "ManageBot"
    Developer = {
        "name":"Abubeker",
        "phone":"+251981566599",
        "telegram_acc":"@abukiw86"
    }
    BOT_VERSION = "1.0.3"
    CREATED_DATE = "2025"
    @classmethod
    def validate(cls):
        """Validate all required configuration."""
        if not cls.BOT_TOKEN:
            logging.error("❌ BOT_TOKEN is missing! Make sure it is set in your environment variables.")
            raise ValueError("BOT_TOKEN is missing! Make sure it is set in your environment variables.")
        
        if cls.BOT_TOKEN == "your_bot_token_here":
            logging.error("❌ Please replace the default BOT_TOKEN with your actual token!")
            raise ValueError("Please replace the default BOT_TOKEN with your actual token!")
        
        logging.info("✅ Configuration validated successfully")
        
    @staticmethod
    def setup_logging():
        """Setup logging configuration."""
        log_level = os.environ.get("LOG_LEVEL", "INFO").upper()
        
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=getattr(logging, log_level, logging.INFO),
            handlers=[
                logging.StreamHandler(sys.stdout), 
                logging.FileHandler('bot.log')
            ]
        )
         
        logging.getLogger("httpx").setLevel(logging.WARNING)
        logging.getLogger("telegram").setLevel(logging.INFO)