# Koyeb Deployment Troubleshooting

## Common Issues and Solutions

### 1. Server Stops When Starting Bot
**Problem**: Clicking "Start Bot" causes the server to stop
**Solution**: 
- Ensure `TELEGRAM_BOT_TOKEN` environment variable is set in Koyeb dashboard
- Check that the token is valid and active
- Bot subprocess may be failing due to missing dependencies

### 2. Environment Variables
**Required Variables**:
- `TELEGRAM_BOT_TOKEN` = `7902520183:AAEUOwfPokeOEhlF9QVGYcMMFuxFcSme7p0`
- `WEB_PASSWORD` = `admin123`
- `FLASK_SECRET_KEY` = Generate random string

### 3. Build Command Issues
**Use this exact build command**:
```bash
pip install -r requirements.txt
```

**Make sure requirements.txt contains**:
```
flask
flask-wtf
wtforms
python-telegram-bot
python-docx
pypdf2
pytesseract
pillow
googletrans==4.0.0rc1
psutil
gunicorn
```

### 4. Start Command
**Use this exact start command**:
```bash
python main.py
```

### 5. Health Check Issues
- Koyeb expects the app to respond on the assigned PORT
- The web dashboard runs on the main process
- Bot runs as subprocess when started from dashboard

### 6. Alternative: Single Process Mode
If subprocess approach fails, consider running bot and web dashboard in the same process (requires code modification).

### 7. Logs and Debugging
- Check Koyeb logs for specific error messages
- Look for import errors or missing dependencies
- Verify bot token is working by testing with a simple script

### 8. File Structure
Ensure all files are in root directory:
- main.py (entry point)
- requirements.txt (dependencies)
- All Python modules
- templates/ folder