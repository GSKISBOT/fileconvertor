"""
Configuration settings for the Telegram bot
"""

import os

# Bot configuration
BOT_TOKEN = os.getenv('TELEGRAM_BOT_TOKEN', '7902520183:AAEUOwfPokeOEhlF9QVGYcMMFuxFcSme7p0')

# File processing settings
MAX_FILE_SIZE = 20 * 1024 * 1024  # 20MB max file size
SUPPORTED_TEXT_FORMATS = ['.txt', '.pdf', '.docx', '.doc', '.rtf', '.odt']
SUPPORTED_IMAGE_FORMATS = ['.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff']

# Translation settings
SUPPORTED_LANGUAGES = {
    'auto': 'Auto-detect',
    'en': 'English',
    'es': 'Spanish',
    'fr': 'French',
    'de': 'German',
    'it': 'Italian',
    'pt': 'Portuguese',
    'ru': 'Russian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh': 'Chinese (Simplified)',
    'zh-tw': 'Chinese (Traditional)',
    'ar': 'Arabic',
    'hi': 'Hindi',
    'ta': 'Tamil',
    'te': 'Telugu',
    'bn': 'Bengali',
    'ur': 'Urdu',
    'th': 'Thai',
    'vi': 'Vietnamese',
    'tr': 'Turkish',
    'pl': 'Polish',
    'nl': 'Dutch',
    'sv': 'Swedish',
    'no': 'Norwegian',
    'da': 'Danish',
    'fi': 'Finnish'
}

# Temporary directory for file processing
TEMP_DIR = os.path.join(os.getcwd(), 'temp')
os.makedirs(TEMP_DIR, exist_ok=True)
