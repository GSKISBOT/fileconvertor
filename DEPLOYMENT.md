# Deployment Guide

## Render Deployment (Recommended)

### Quick Deploy Button
Click this button to deploy directly to Render:

[![Deploy to Render](https://render.com/images/deploy-to-render-button.svg)](https://render.com/deploy)

### Manual Deployment Steps

1. **Prepare Repository**
   ```bash
   git clone <your-repo>
   cd telegram-bot
   ```

2. **Create Web Service on Render**
   - Repository: Your GitHub repo
   - Branch: `main`
   - Runtime: `Python 3`
   - Build Command: `pip install -r requirements.txt && apt-get update && apt-get install -y tesseract-ocr`
   - Start Command: `gunicorn web_dashboard:app --bind 0.0.0.0:$PORT`

3. **Environment Variables**
   ```
   TELEGRAM_BOT_TOKEN=your_bot_token_here
   WEB_PASSWORD=admin123
   FLASK_SECRET_KEY=generate_random_key
   ```

4. **Health Check**
   - Path: `/health`
   - Render will automatically monitor this endpoint

## Alternative Deployments

### Heroku
```bash
# Install Heroku CLI
heroku create your-app-name
heroku buildpacks:set heroku/python
heroku buildpacks:add --index 1 heroku-community/apt
heroku config:set TELEGRAM_BOT_TOKEN=your_token
heroku config:set WEB_PASSWORD=admin123
heroku config:set FLASK_SECRET_KEY=$(openssl rand -base64 32)
git push heroku main
