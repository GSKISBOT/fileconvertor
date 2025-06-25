# Telegram File Converter & Translator Bot

## Overview

This is a Python-based Telegram bot that provides file conversion and translation services with a web dashboard for management. The bot can convert various file formats (text files, PDFs, Word documents, images) to DOCX format and translate documents between 50+ languages including Tamil, Spanish, French, and more. The system includes OCR capabilities for extracting text from images and a Flask-based web interface for managing authorized users and bot operations.

## System Architecture

The application follows a modular microservice-like architecture with clear separation of concerns:

- **Bot Interface Layer**: Handles Telegram bot interactions using python-telegram-bot v22.1+ with async/await patterns
- **Service Layer**: Contains business logic for file conversion and translation services
- **Web Dashboard Layer**: Flask-based web interface for bot management and user administration
- **Utility Layer**: Provides common helper functions and file operations
- **Configuration Layer**: Environment variable-based configuration management

## Key Components

### 1. Telegram Bot Interface (`bot.py`, `main.py`)
- **Purpose**: Main Telegram bot implementation with inline keyboard interface
- **Architecture Decision**: Uses python-telegram-bot v22.1+ library with async/await patterns for modern Python compatibility
- **Key Features**: Command handlers, callback query handlers, file processing handlers, user authorization system
- **Rationale**: Provides a user-friendly interface with inline keyboards for better UX while leveraging modern async Python features

### 2. File Converter (`file_converter.py`)
- **Purpose**: Handles conversion of various file formats to DOCX
- **Supported Formats**: TXT, PDF, DOC/DOCX, RTF, ODT, and image formats (JPG, PNG, TIFF, etc.)
- **Architecture Decision**: Uses specialized libraries for each file type (PyPDF2 for PDFs, pytesseract for OCR, python-docx for Word documents)
- **External Dependencies**: Tesseract OCR engine for image text extraction
- **Rationale**: Modular approach allows for easy extension of supported formats while maintaining high conversion quality

### 3. Translator (`translator.py`)
- **Purpose**: Provides translation services using Google Translate API
- **Architecture Decision**: Uses googletrans library for translation services with chunking for large texts
- **Features**: Auto-detection of source language, chunked translation for large texts (5000 char limit), DOCX output generation
- **Rationale**: Leverages Google's robust translation service for high-quality results while handling API limitations

### 4. Web Dashboard (`web_dashboard.py`)
- **Purpose**: Flask-based web interface for bot management and user administration
- **Architecture Decision**: Separate web service that can run independently or alongside the bot
- **Key Features**: User authentication, authorized user management, bot start/stop controls, system status monitoring
- **Security**: Password-based authentication with session management, CSRF protection disabled for simplified deployment
- **Rationale**: Provides administrative interface without requiring direct server access

### 5. Configuration (`config.py`)
- **Purpose**: Centralized configuration management
- **Settings**: Bot token, file size limits (20MB), supported formats and languages, temporary directory management
- **Architecture Decision**: Environment variable-based configuration for security and deployment flexibility
- **Rationale**: Makes the application configurable without code changes and keeps sensitive data secure

### 6. Utilities (`utils.py`)
- **Purpose**: Common helper functions for file operations
- **Functions**: File cleanup, extension detection, size formatting, filename sanitization, file type validation
- **Architecture Decision**: Separated utility functions for reusability across components
- **Rationale**: Promotes code reuse, maintainability, and consistent file handling

## Data Flow

1. **User Interaction**: User sends commands or files to the Telegram bot
2. **Authorization Check**: Bot verifies user ID against authorized users list (JSON file)
3. **File Processing**: 
   - File download from Telegram servers to temporary storage
   - Format detection and appropriate converter selection
   - Text extraction or OCR processing
   - DOCX generation with converted content
4. **Translation Flow** (if requested):
   - Text extraction from source file
   - Language detection using Google Translate
   - Chunked translation to handle API limits
   - DOCX generation with translated content
5. **Response**: Processed file sent back to user via Telegram
6. **Cleanup**: Temporary files automatically removed after processing

## External Dependencies

### Core Libraries
- **python-telegram-bot v22.1+**: Modern async Telegram bot framework
- **Flask**: Web framework for dashboard interface
- **python-docx**: Microsoft Word document generation and manipulation
- **PyPDF2**: PDF text extraction
- **Pillow (PIL)**: Image processing and manipulation
- **pytesseract**: Python wrapper for Tesseract OCR engine
- **googletrans**: Google Translate API client

### System Dependencies
- **Tesseract OCR**: Required for image text extraction (installed via system packages)
- **PostgreSQL**: Database support included in deployment configuration
- **Gunicorn**: WSGI HTTP server for production deployment

### Development Tools
- **Flask-WTF**: Form handling and CSRF protection
- **psutil**: System process monitoring
- **WTForms**: Form validation and rendering

## Deployment Strategy

### Primary Platform: Render
- **Configuration**: `render.yaml` provides one-click deployment configuration
- **Build Process**: Automated pip installation with system package installation (tesseract-ocr)
- **Runtime**: Python 3.11.9 with Gunicorn WSGI server
- **Environment Variables**: Secure storage of bot token, web password, and Flask secret key
- **Health Monitoring**: Built-in health check endpoint at `/health`

### Alternative Platforms
- **Heroku**: Procfile and buildpack configuration provided
- **Railway**: Compatible with Python runtime detection
- **Replit**: `.replit` configuration for development and testing

### Deployment Considerations
- **Scaling**: Autoscale configuration for handling variable load
- **Security**: Environment variable-based secrets management
- **Monitoring**: Process monitoring via psutil and web dashboard
- **File Storage**: Temporary file handling with automatic cleanup

### Environment Configuration
- `TELEGRAM_BOT_TOKEN`: Bot authentication token from BotFather
- `WEB_PASSWORD`: Dashboard access password (default: admin123)
- `FLASK_SECRET_KEY`: Session encryption key (auto-generated recommended)

## Changelog

- June 25, 2025: Initial setup and full implementation completed
  - Fixed port conflicts between Flask web dashboard and Telegram bot
  - Configured bot token and authorized users
  - Created beautiful web interface with custom styling
  - Bot successfully starts/stops from dashboard
  - All file conversion and translation features functional
  - Fixed Render deployment compatibility by updating ParseMode import
  - Updated build command with user's specific pip install requirements
  - Added comprehensive deployment instructions for Render
  - Fixed Koyeb deployment issue by adding requirements.txt file
  - Created deployment packages for multiple free hosting platforms

## User Preferences

Preferred communication style: Simple, everyday language.