#!/usr/bin/env python3
"""
Flask web application entry point for the Telegram bot dashboard
"""

import os
import logging
from web_dashboard import app

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# This allows gunicorn to find the Flask app
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    logger.info(f"Starting web dashboard on port {port}")
    
    # Check required environment variables
    if not os.getenv('TELEGRAM_BOT_TOKEN'):
        logger.warning("TELEGRAM_BOT_TOKEN not set - bot functionality will be limited")
    
    app.run(host='0.0.0.0', port=port, debug=False)
