# Render Deployment Instructions

## Build Command
```bash
python -m pip install --upgrade pip && pip install --pre --only-binary=all --extra-index-url https://pypi.anaconda.org/simple/ flask flask-wtf wtforms python-telegram-bot python-docx pypdf2 pytesseract pillow googletrans psutil gunicorn
```

## Start Command
```bash
python main.py
```

## Environment Variables
Set these in your Render dashboard:

- `TELEGRAM_BOT_TOKEN` = `7902520183:AAEUOwfPokeOEhlF9QVGYcMMFuxFcSme7p0`
- `WEB_PASSWORD` = `admin123` (or your preferred password)
- `FLASK_SECRET_KEY` = Generate a random string

## Manual Setup Steps
1. Create new Web Service on Render
2. Connect your repository or upload zip file
3. Use Python environment
4. Copy the build command above
5. Copy the start command above
6. Add environment variables
7. Deploy

## Features
- Web dashboard at your Render URL
- Login with password to manage bot
- Start/stop bot from web interface
- File conversion: PDF, TXT, DOC to DOCX
- Translation: 50+ languages
- OCR: Extract text from images
- User authorization system

## Troubleshooting
- If deployment fails, check logs for specific errors
- Ensure all environment variables are set correctly
- Bot will only respond to authorized user IDs: 6495752999, 7122689824, 6223225776