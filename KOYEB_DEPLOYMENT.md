# Koyeb Deployment Instructions

## Quick Setup
1. Connect your GitHub repository to Koyeb
2. Select Python runtime
3. **IMPORTANT**: Rename `requirements_koyeb.txt` to `requirements.txt` in your repository
4. Use these settings:

## Build Settings
- **Build Command**: `pip install -r requirements.txt`
- **Start Command**: `python main.py`

## Environment Variables
Set these in Koyeb dashboard:
- `TELEGRAM_BOT_TOKEN` = `7902520183:AAEUOwfPokeOEhlF9QVGYcMMFuxFcSme7p0`
- `WEB_PASSWORD` = `admin123`
- `FLASK_SECRET_KEY` = Generate random string
- `PORT` = `8000` (Koyeb will auto-assign)

## Files Required
- `requirements.txt` ✓ (included)
- `runtime.txt` ✓ (Python 3.11)
- `main.py` ✓ (entry point)

## Features
- Free tier: 2 services, always-on
- Automatic HTTPS
- Global CDN
- No credit card required
- Only email signup needed

## Troubleshooting
- Ensure all files are committed to Git
- Check environment variables are set
- Bot responds only to authorized users: 6495752999, 7122689824, 6223225776