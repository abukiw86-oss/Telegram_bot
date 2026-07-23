import os
from dotenv import load_dotenv
import logging

load_dotenv()

class Config:
    BOT_TOKEN = os.environ.get("BOT_TOKEN")
    DEFAULT_EXPIRY_YEARS = 10
    
    @classmethod
    def validate(cls):
        if not cls.BOT_TOKEN:
            raise ValueError("BOT_TOKEN is missing! Make sure it is set in your .env file or environment.")
        
    @staticmethod
    def setup_logging():
        logging.basicConfig(
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            level=logging.INFO
        )