# Telegram File Converter & Translator Bot - Quick Start Guide

A powerful Telegram bot that converts files to DOCX format and translates documents between multiple languages, with a web dashboard for easy management.

## Features

- **File Conversion**: Convert PDF, TXT, RTF, DOC, ODT, and image files to DOCX
- **File Translation**: Translate documents to 50+ languages including Tamil, Spanish, French, etc.
- **OCR Support**: Extract text from images using advanced OCR
- **Web Dashboard**: Manage authorized users and bot status through a web interface
- **Access Control**: Restrict bot usage to authorized Telegram users only

## Quick Deploy to Render

### Step 1: Get Your Telegram Bot Token

1. Message [@BotFather](https://t.me/botfather) on Telegram
2. Send `/newbot` and follow the prompts
3. Copy your bot token (looks like `123456789:ABCdefGHIjklMNOpqrsTUVwxyz`)

### Step 2: Deploy to Render

1. **Fork this repository** to your GitHub account

2. **Create a new Web Service on Render**:
   - Go to [render.com](https://render.com) and sign up/login
   - Click "New" → "Web Service"
   - Connect your GitHub repository

3. **Configure the deployment**:
   - **Name**: `telegram-bot-dashboard`
   - **Environment**: `Python 3`
   - **Build Command**: `pip install -r requirements.txt && apt-get update && apt-get install -y tesseract-ocr`
   - **Start Command**: `gunicorn web_dashboard:app --bind 0.0.0.0:$PORT`

4. **Set Environment Variables**:
   - `TELEGRAM_BOT_TOKEN`: Your bot token from Step 1
   - `WEB_PASSWORD`: `admin123` (or choose your own password)
   - `FLASK_SECRET_KEY`: Click "Generate" for a random key

5. **Deploy**: Click "Create Web Service"

### Step 3: Configure Your Bot

1. **Access the Dashboard**:
   - Once deployed, visit your Render URL (e.g., `https://your-app.onrender.com`)
   - Login with password `admin123` (or your custom password)

2. **Add Authorized Users**:
   - Start a chat with your bot on Telegram
   - Send `/start` to get your User ID
   - Add your User ID in the web dashboard
   - Click "Start Bot" in the dashboard

3. **Test Your Bot**:
   - Send `/start` to your bot on Telegram
   - Try uploading a file to convert or translate

## Usage

### File Conversion
1. Send `/start` to your bot
2. Click "Convert Any File to DOCX"
3. Upload any supported file
4. Receive converted DOCX file

### File Translation
1. Send `/start` to your bot
2. Click "Translate File to Any Language"
3. Upload a file with text
4. Choose target language
5. Receive translated DOCX file

### Supported File Types
- **Documents**: PDF, DOC, DOCX, TXT, RTF, ODT
- **Images**: JPG, PNG, GIF, BMP, TIFF (with OCR)
- **Text**: Direct text messages

### Supported Languages
- **Popular**: English, Spanish, French, German, Chinese, Japanese, Tamil
- **50+ total languages** including Arabic, Hindi, Russian, Portuguese, and more

## Web Dashboard Features

- **Bot Control**: Start/stop the Telegram bot
- **User Management**: Add/remove authorized Telegram user IDs
- **Status Monitoring**: View bot status and logs
- **Secure Access**: Password-protected admin panel

## Environment Variables

| Variable | Required | Description |
|----------|----------|-------------|
| `TELEGRAM_BOT_TOKEN` | Yes | Your bot token from BotFather |
| `WEB_PASSWORD` | No | Dashboard password (default: admin123) |
| `FLASK_SECRET_KEY` | Yes | Flask session security key |

## Troubleshooting

### Bot Not Responding
1. Check if bot is started in the web dashboard
2. Verify your Telegram bot token is correct
3. Ensure your User ID is added to authorized users

### Files Not Processing
1. Check file size (max 20MB)
2. Verify file format is supported
3. For images, ensure text is clear and readable

### Web Dashboard Issues
1. Check environment variables are set correctly
2. Verify the service is running on Render
3. Try restarting the service from Render dashboard

## Technical Details

- **Python 3.11** with Flask web framework
- **Async Telegram Bot** using python-telegram-bot v22.1+ library
- **OCR**: Tesseract for image text extraction
- **Translation**: Google Translate API
- **Deployment**: Render with auto-scaling

## Security

- User authorization required for bot access
- Password-protected web dashboard
- Secure file handling with automatic cleanup
- Environment variable based configuration

## Support

For issues or questions:
1. Check the troubleshooting section above
2. Review Render deployment logs
3. Verify all environment variables are set correctly

---

**Ready to deploy?** Follow the 3 steps above and your bot will be live in minutes!
