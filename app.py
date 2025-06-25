#!/usr/bin/env python3
"""
Main entry point for the Telegram File Conversion and Translation Bot
"""

import logging
import os
from bot import TelegramBot

# Configure logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    level=logging.INFO
)
logger = logging.getLogger(__name__)

def main():
    """Main function to start the bot"""
    try:
        # Check if bot token is available
        from config import BOT_TOKEN
        if not BOT_TOKEN:
            logger.error("TELEGRAM_BOT_TOKEN environment variable is not set!")
            print("Error: TELEGRAM_BOT_TOKEN environment variable is not set!")
            return
        
        logger.info(f"Starting bot with token: {BOT_TOKEN[:10]}...")
        
        # Initialize and start the bot
        bot = TelegramBot()
        bot.run()
    except Exception as e:
        logger.error(f"Failed to start bot: {e}")
        print(f"Error starting bot: {e}")
        raise

if __name__ == '__main__':
    main()