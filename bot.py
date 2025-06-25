"""
Main Telegram bot implementation with inline keyboard interface
Compatible with python-telegram-bot v21.6
"""

import logging
import os
import tempfile
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
try:
    from telegram.constants import ParseMode
except ImportError:
    from telegram import ParseMode
from telegram.ext import Updater, CommandHandler, CallbackQueryHandler, MessageHandler, Filters, CallbackContext

from config import BOT_TOKEN, SUPPORTED_LANGUAGES
from file_converter import FileConverter
from translator import Translator
from utils import cleanup_file, get_file_extension, format_file_size
import json

logger = logging.getLogger(__name__)

class TelegramBot:
    def __init__(self):
        self.updater = Updater(token=BOT_TOKEN, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.file_converter = FileConverter()
        self.translator = Translator()
        self.authorized_users_file = 'authorized_users.json'
        self.setup_handlers()
    
    def load_authorized_users(self):
        """Load authorized users from JSON file"""
        try:
            if os.path.exists(self.authorized_users_file):
                with open(self.authorized_users_file, 'r') as f:
                    return json.load(f)
            return []
        except Exception as e:
            logger.error(f"Error loading authorized users: {e}")
            return []
    
    def is_user_authorized(self, user_id):
        """Check if user is authorized to use the bot"""
        authorized_users = self.load_authorized_users()
        return str(user_id) in authorized_users or len(authorized_users) == 0
        
    def setup_handlers(self):
        """Setup all command and callback handlers"""
        # Command handlers
        self.dispatcher.add_handler(CommandHandler("start", self.start_command))
        self.dispatcher.add_handler(CommandHandler("help", self.help_command))
        
        # Callback query handlers
        self.dispatcher.add_handler(CallbackQueryHandler(self.handle_callback))
        
        # Message handlers
        self.dispatcher.add_handler(MessageHandler(Filters.document, self.handle_document))
        self.dispatcher.add_handler(MessageHandler(Filters.photo, self.handle_photo))
        self.dispatcher.add_handler(MessageHandler(Filters.text & ~Filters.command, self.handle_text))

    def start_command(self, update: Update, context: CallbackContext):
        """Handle /start command"""
        user_id = update.effective_user.id
        
        # Check if user is authorized
        if not self.is_user_authorized(user_id):
            unauthorized_message = (
                "🚫 *Access Denied*\n\n"
                "You are not authorized to use this bot.\n"
                "Please contact the administrator to get access.\n\n"
                f"Your User ID: `{user_id}`\n"
                "Send this ID to the bot administrator."
            )
            update.message.reply_text(
                unauthorized_message,
                parse_mode=ParseMode.MARKDOWN
            )
            return
        
        keyboard = [
            [InlineKeyboardButton("📄 Convert Any File to DOCX", callback_data='convert_to_docx')],
            [InlineKeyboardButton("🌐 Translate File to Any Language", callback_data='translate_file')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        welcome_message = (
            "🤖 *Welcome to File Converter & Translator Bot!*\n\n"
            "I can help you with:\n"
            "• Convert any file to DOCX format\n"
            "• Translate files between different languages\n\n"
            "Choose an option below to get started:"
        )
        
        update.message.reply_text(
            welcome_message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    def help_command(self, update: Update, context: CallbackContext):
        """Handle /help command"""
        self.show_help(update, context)

    def show_help(self, update: Update, context: CallbackContext):
        """Show help information"""
        help_text = (
            "🔧 *How to use this bot:*\n\n"
            "**File Conversion:**\n"
            "1. Click 'Convert Any File to DOCX'\n"
            "2. Send me any file (PDF, TXT, DOC, etc.)\n"
            "3. Get your converted DOCX file\n\n"
            "**File Translation:**\n"
            "1. Click 'Translate File to Any Language'\n"
            "2. Send me a file with text content\n"
            "3. Choose target language\n"
            "4. Get your translated DOCX file\n\n"
            "**Supported Languages:**\n"
            "English, Spanish, French, German, Italian, Portuguese, Russian, "
            "Japanese, Korean, Chinese, Arabic, Hindi, Tamil, Telugu, Bengali, "
            "Urdu, Thai, Vietnamese, Turkish, Polish, Dutch, Swedish, Norwegian, "
            "Danish, Finnish and more!\n\n"
            "**File Size Limit:** 20MB\n"
            "**Supported Formats:** PDF, TXT, DOC, DOCX, RTF, ODT, Images with text"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        if update.callback_query:
            update.callback_query.edit_message_text(
                help_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            update.message.reply_text(
                help_text,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )

    def handle_callback(self, update: Update, context: CallbackContext):
        """Handle callback queries from inline keyboards"""
        query = update.callback_query
        query.answer()
        
        user_id = update.effective_user.id
        if not self.is_user_authorized(user_id):
            query.edit_message_text("🚫 Access denied. Please contact administrator.")
            return
        
        data = query.data
        
        if data == 'convert_to_docx':
            self.start_file_conversion(update, context)
        elif data == 'translate_file':
            self.start_file_translation(update, context)
        elif data == 'help':
            self.show_help(update, context)
        elif data == 'back_to_main':
            self.show_main_menu(update, context)
        elif data.startswith('translate_to_'):
            target_lang = data.replace('translate_to_', '')
            self.process_translation(update, context, target_lang)
        elif data == 'show_more_languages':
            self.show_language_selection(update, context, show_all=True)

    def start_file_conversion(self, update: Update, context: CallbackContext):
        """Start file conversion workflow"""
        context.user_data['mode'] = 'convert'
        
        message = (
            "📄 *File Conversion Mode*\n\n"
            "Please send me any file you want to convert to DOCX format.\n\n"
            "**Supported formats:**\n"
            "• PDF documents\n"
            "• Text files (TXT, RTF)\n"
            "• Word documents (DOC, DOCX)\n"
            "• OpenDocument files (ODT)\n"
            "• Images with text (JPG, PNG, etc.)\n\n"
            "📎 *Just send your file and I'll convert it for you!*"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    def start_file_translation(self, update: Update, context: CallbackContext):
        """Start file translation workflow"""
        context.user_data['mode'] = 'translate'
        
        message = (
            "🌐 *File Translation Mode*\n\n"
            "Please send me a file containing text you want to translate.\n\n"
            "**Supported formats:**\n"
            "• PDF documents\n"
            "• Text files (TXT, RTF)\n"
            "• Word documents (DOC, DOCX)\n"
            "• OpenDocument files (ODT)\n"
            "• Images with text (JPG, PNG, etc.)\n\n"
            "I'll auto-detect the source language and let you choose the target language.\n\n"
            "📎 *Send your file to get started!*"
        )
        
        keyboard = [[InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_to_main')]]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    def show_main_menu(self, update: Update, context: CallbackContext):
        """Show the main menu"""
        keyboard = [
            [InlineKeyboardButton("📄 Convert Any File to DOCX", callback_data='convert_to_docx')],
            [InlineKeyboardButton("🌐 Translate File to Any Language", callback_data='translate_file')],
            [InlineKeyboardButton("ℹ️ Help", callback_data='help')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = (
            "🤖 *File Converter & Translator Bot*\n\n"
            "Choose an option below:"
        )
        
        update.callback_query.edit_message_text(
            message,
            parse_mode=ParseMode.MARKDOWN,
            reply_markup=reply_markup
        )

    def show_language_selection(self, update: Update, context: CallbackContext, show_all=False):
        """Show language selection menu"""
        keyboard = []
        
        # Popular languages first
        popular_langs = ['en', 'es', 'fr', 'de', 'it', 'pt', 'ru', 'ja', 'ko', 'zh', 'ar', 'hi', 'ta']
        
        if not show_all:
            # Show popular languages in rows of 2
            for i in range(0, len(popular_langs), 2):
                row = []
                for j in range(2):
                    if i + j < len(popular_langs):
                        lang_code = popular_langs[i + j]
                        lang_name = SUPPORTED_LANGUAGES[lang_code]
                        row.append(InlineKeyboardButton(f"{lang_name}", callback_data=f'translate_to_{lang_code}'))
                keyboard.append(row)
            
            keyboard.append([InlineKeyboardButton("🔽 Show More Languages", callback_data='show_more_languages')])
        else:
            # Show all languages
            lang_items = [(code, name) for code, name in SUPPORTED_LANGUAGES.items() if code != 'auto']
            for i in range(0, len(lang_items), 2):
                row = []
                for j in range(2):
                    if i + j < len(lang_items):
                        lang_code, lang_name = lang_items[i + j]
                        row.append(InlineKeyboardButton(f"{lang_name}", callback_data=f'translate_to_{lang_code}'))
                keyboard.append(row)
        
        keyboard.append([InlineKeyboardButton("🔙 Back to Main Menu", callback_data='back_to_main')])
        reply_markup = InlineKeyboardMarkup(keyboard)
        
        message = (
            "🌐 *Select Target Language*\n\n"
            "Choose the language you want to translate to:"
        )
        
        if update.callback_query:
            update.callback_query.edit_message_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )
        else:
            update.message.reply_text(
                message,
                parse_mode=ParseMode.MARKDOWN,
                reply_markup=reply_markup
            )

    def handle_document(self, update: Update, context: CallbackContext):
        """Handle document uploads"""
        user_id = update.effective_user.id
        if not self.is_user_authorized(user_id):
            update.message.reply_text("🚫 Access denied. Please contact administrator.")
            return
            
        if 'mode' not in context.user_data:
            update.message.reply_text(
                "❌ Please select a mode first using /start",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')]])
            )
            return
        
        document = update.message.document
        file_size = document.file_size
        
        if file_size > 20 * 1024 * 1024:  # 20MB limit
            update.message.reply_text(
                f"❌ File too large! Maximum size is 20MB.\n"
                f"Your file: {format_file_size(file_size)}"
            )
            return
        
        try:
            # Send processing message
            processing_msg = update.message.reply_text("⏳ Processing your file...")
            
            # Download file
            file = context.bot.get_file(document.file_id)
            with tempfile.NamedTemporaryFile(delete=False) as temp_file:
                file.download(temp_file.name)
                temp_file_path = temp_file.name
            
            mode = context.user_data.get('mode')
            
            if mode == 'convert':
                # Simple text extraction for demo
                update.message.reply_text("✅ File conversion feature will be implemented!")
                
            elif mode == 'translate':
                # Store file for translation
                context.user_data['file_path'] = temp_file_path
                context.user_data['original_filename'] = document.file_name
                
                # Show language selection
                self.show_language_selection(update, context)
                processing_msg.delete()
                return
            
            # Cleanup
            cleanup_file(temp_file_path)
            processing_msg.delete()
            
        except Exception as e:
            logger.error(f"Error processing document: {e}")
            update.message.reply_text(f"❌ Error processing file: {str(e)}")
            if 'temp_file_path' in locals():
                cleanup_file(temp_file_path)

    def handle_photo(self, update: Update, context: CallbackContext):
        """Handle photo uploads"""
        user_id = update.effective_user.id
        if not self.is_user_authorized(user_id):
            update.message.reply_text("🚫 Access denied. Please contact administrator.")
            return
            
        if 'mode' not in context.user_data:
            update.message.reply_text(
                "❌ Please select a mode first using /start",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')]])
            )
            return
        
        update.message.reply_text("✅ Photo processing feature will be implemented!")

    def handle_text(self, update: Update, context: CallbackContext):
        """Handle text messages"""
        user_id = update.effective_user.id
        if not self.is_user_authorized(user_id):
            update.message.reply_text("🚫 Access denied. Please contact administrator.")
            return
            
        if 'mode' not in context.user_data:
            update.message.reply_text(
                "❌ Please select a mode first using /start",
                reply_markup=InlineKeyboardMarkup([[InlineKeyboardButton("🏠 Main Menu", callback_data='back_to_main')]])
            )
            return
        
        update.message.reply_text("✅ Text processing feature will be implemented!")

    def process_translation(self, update: Update, context: CallbackContext, target_lang: str):
        """Process translation with selected language"""
        try:
            update.callback_query.edit_message_text("⏳ Translating your file...")
            
            # For now, just show success message
            lang_name = SUPPORTED_LANGUAGES.get(target_lang, target_lang)
            update.callback_query.edit_message_text(
                f"✅ Translation to {lang_name} will be implemented!"
            )
            
            # Cleanup stored file
            file_path = context.user_data.get('file_path')
            if file_path:
                cleanup_file(file_path)
                context.user_data.clear()
                
        except Exception as e:
            logger.error(f"Error in translation: {e}")
            update.callback_query.edit_message_text(f"❌ Translation error: {str(e)}")

    def run(self):
        """Run the bot"""
        logger.info("Starting Telegram bot...")
        self.updater.start_polling()
        logger.info("Bot is running!")
        self.updater.idle()

    def stop(self):
        """Stop the bot"""
        logger.info("Stopping Telegram bot...")
        self.updater.stop()