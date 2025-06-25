"""
Web dashboard for managing Telegram bot on Render deployment
Updated for python-telegram-bot v22.1+ async compatibility
"""

import os
import json
import logging
import asyncio
import signal
import threading
import time
from datetime import datetime
from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired
import subprocess
import psutil

app = Flask(__name__)
app.secret_key = os.getenv('FLASK_SECRET_KEY', 'your-secret-key-change-this-in-production')

# Configure Flask-WTF - disable CSRF for now to fix login issues
app.config['WTF_CSRF_ENABLED'] = False
app.config['SECRET_KEY'] = app.secret_key

# Enable debug mode to see detailed error messages
if os.getenv('FLASK_DEBUG', 'False').lower() == 'true':
    app.debug = True

# Configuration
WEB_PASSWORD = os.getenv('WEB_PASSWORD', 'admin123')
AUTHORIZED_USERS_FILE = 'authorized_users.json'

# Global variables
bot_process = None
bot_running = False

# Initialize bot status on startup
def initialize_bot_status():
    """Initialize bot running status on startup"""
    global bot_running, bot_process
    bot_running = is_bot_running()
    if not bot_running:
        bot_process = None

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class LoginForm(FlaskForm):
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

class UserForm(FlaskForm):
    user_id = StringField('User ID', validators=[DataRequired()])
    submit = SubmitField('Add User')

def load_authorized_users():
    """Load authorized users from JSON file"""
    try:
        if os.path.exists(AUTHORIZED_USERS_FILE):
            with open(AUTHORIZED_USERS_FILE, 'r') as f:
                return json.load(f)
        return []
    except Exception as e:
        logger.error(f"Error loading authorized users: {e}")
        return []

def save_authorized_users(users):
    """Save authorized users to JSON file"""
    try:
        with open(AUTHORIZED_USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)
        return True
    except Exception as e:
        logger.error(f"Error saving authorized users: {e}")
        return False

def is_bot_running():
    """Check if bot is currently running"""
    global bot_process, bot_running
    try:
        # First check if we have a tracked process that's still running
        if bot_process and bot_process.poll() is None:
            bot_running = True
            return True
        
        # Check system processes for any running bot (app.py)
        import psutil
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'] and proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    # Look for app.py (bot entry point) but exclude this web dashboard
                    if 'app.py' in cmdline and 'main.py' not in cmdline:
                        bot_running = True
                        return True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # No bot process found
        bot_running = False
        bot_process = None
        return False
    except Exception as e:
        logger.error(f"Error checking bot status: {e}")
        bot_running = False
        return False

def start_bot():
    """Start the Telegram bot"""
    global bot_process, bot_running
    try:
        # First stop any existing bot instances
        stop_bot()
        
        # Kill any existing python main.py processes
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'] and proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'main.py' in cmdline:
                        proc.terminate()
                        try:
                            proc.wait(timeout=5)
                        except psutil.TimeoutExpired:
                            proc.kill()
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        # Wait a moment to ensure processes are terminated
        time.sleep(2)
        
        # Start new bot process with environment variables
        env = os.environ.copy()
        env['TELEGRAM_BOT_TOKEN'] = '7902520183:AAEUOwfPokeOEhlF9QVGYcMMFuxFcSme7p0'
        bot_process = subprocess.Popen(['python', 'app.py'], 
                                     env=env,
                                     stdout=subprocess.PIPE, 
                                     stderr=subprocess.PIPE,
                                     cwd=os.getcwd())
        
        # Wait a moment to check if bot started successfully
        time.sleep(3)
        
        # Check if process is still running
        if bot_process.poll() is None:
            bot_running = True
            logger.info("Bot started successfully")
            return True
        else:
            # Bot process died, get error output
            stdout, stderr = bot_process.communicate()
            error_msg = stderr.decode() if stderr else stdout.decode()
            
            # Check for port conflict
            if "Address already in use" in error_msg:
                logger.error("Bot failed to start: Address already in use\nPort 5000 is in use by another program. Either identify and stop that program, or start the server with a different port.")
            else:
                logger.error(f"Bot failed to start: {error_msg}")
            bot_running = False
            return False
    except Exception as e:
        logger.error(f"Error starting bot: {e}")
        bot_running = False
        return False

def stop_bot():
    """Stop the Telegram bot"""
    global bot_process, bot_running
    try:
        # Stop the tracked process
        if bot_process and bot_process.poll() is None:
            bot_process.terminate()
            try:
                bot_process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                bot_process.kill()
                bot_process.wait()
        
        # Also kill any python main.py processes
        killed_any = False
        for proc in psutil.process_iter(['pid', 'name', 'cmdline']):
            try:
                if 'python' in proc.info['name'] and proc.info['cmdline']:
                    cmdline = ' '.join(proc.info['cmdline'])
                    if 'main.py' in cmdline:
                        proc.terminate()
                        try:
                            proc.wait(timeout=5)
                        except psutil.TimeoutExpired:
                            proc.kill()
                        killed_any = True
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
        
        bot_running = False
        if killed_any:
            logger.info("Bot stopped successfully")
        else:
            logger.info("Bot was not running")
        return True
    except Exception as e:
        logger.error(f"Error stopping bot: {e}")
        return False

def requires_auth(f):
    """Decorator for routes that require authentication"""
    def decorated_function(*args, **kwargs):
        if not session.get('authenticated'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

@app.route('/')
def index():
    """Main dashboard page"""
    if not session.get('authenticated'):
        return redirect(url_for('login'))
    
    # Initialize and check bot status
    initialize_bot_status()
    bot_status = is_bot_running()
    authorized_users = load_authorized_users()
    user_form = UserForm()
    
    return render_template('dashboard.html', 
                         bot_running=bot_status,
                         authorized_users=authorized_users,
                         user_count=len(authorized_users),
                         user_form=user_form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    """Login page"""
    form = LoginForm()
    if form.validate_on_submit():
        if form.password.data == WEB_PASSWORD:
            session['authenticated'] = True
            flash('Successfully logged in!', 'success')
            return redirect(url_for('index'))
        else:
            flash('Invalid password!', 'error')
    
    # Show bot status on login page
    bot_status = is_bot_running()
    return render_template('login.html', form=form, bot_running=bot_status)

@app.route('/logout')
def logout():
    """Logout and clear session"""
    session.clear()
    flash('Successfully logged out!', 'info')
    return redirect(url_for('login'))

@app.route('/start_bot', methods=['POST'])
@requires_auth
def start_bot_route():
    """Start the bot"""
    if start_bot():
        flash('Bot started successfully!', 'success')
    else:
        flash('Failed to start bot!', 'error')
    return redirect(url_for('index'))

@app.route('/stop_bot', methods=['POST'])
@requires_auth
def stop_bot_route():
    """Stop the bot"""
    if stop_bot():
        flash('Bot stopped successfully!', 'success')
    else:
        flash('Failed to stop bot!', 'error')
    return redirect(url_for('index'))

@app.route('/add_user', methods=['POST'])
@requires_auth
def add_user():
    """Add authorized user"""
    try:
        form = UserForm()
        if form.validate_on_submit():
            user_id = form.user_id.data.strip()
            if user_id.isdigit():
                users = load_authorized_users()
                if user_id not in users:
                    users.append(user_id)
                    if save_authorized_users(users):
                        flash(f'User {user_id} added successfully!', 'success')
                    else:
                        flash('Failed to save user!', 'error')
                else:
                    flash('User already exists!', 'warning')
            else:
                flash('User ID must be numeric!', 'error')
        else:
            # Try to get user_id from raw form data if WTF validation fails
            user_id = request.form.get('user_id', '').strip()
            if user_id and user_id.isdigit():
                users = load_authorized_users()
                if user_id not in users:
                    users.append(user_id)
                    if save_authorized_users(users):
                        flash(f'User {user_id} added successfully!', 'success')
                    else:
                        flash('Failed to save user!', 'error')
                else:
                    flash('User already exists!', 'warning')
            else:
                flash('Please enter a valid numeric User ID!', 'error')
    except Exception as e:
        logger.error(f"Error adding user: {e}")
        flash('Error adding user!', 'error')
    
    return redirect(url_for('index'))

@app.route('/remove_user/<user_id>', methods=['POST'])
@requires_auth
def remove_user(user_id):
    """Remove authorized user"""
    try:
        users = load_authorized_users()
        if user_id in users:
            users.remove(user_id)
            if save_authorized_users(users):
                flash(f'User {user_id} removed successfully!', 'success')
            else:
                flash('Failed to remove user!', 'error')
        else:
            flash('User not found!', 'warning')
    except Exception as e:
        logger.error(f"Error removing user {user_id}: {e}")
        flash('Error removing user!', 'error')
    
    return redirect(url_for('index'))

@app.route('/api/status')
@requires_auth
def api_status():
    """API endpoint for bot status"""
    return jsonify({
        'bot_running': is_bot_running(),
        'user_count': len(load_authorized_users()),
        'timestamp': datetime.now().isoformat()
    })

@app.route('/health')
def health():
    """Health check endpoint for Render"""
    return jsonify({
        'status': 'healthy',
        'timestamp': datetime.now().isoformat()
    })

@app.route('/api/public-status')
def public_status():
    """Public API endpoint for bot status (no auth required)"""
    try:
        status = is_bot_running()
        logger.info(f"Bot status check: {status}")
        return jsonify({
            'bot_running': status,
            'timestamp': datetime.now().isoformat(),
            'status_text': 'Running' if status else 'Stopped'
        })
    except Exception as e:
        logger.error(f"Error checking bot status: {e}")
        return jsonify({
            'bot_running': False,
            'timestamp': datetime.now().isoformat(),
            'status_text': 'Error'
        })

@app.route('/api/public-start-bot', methods=['POST'])
def public_start_bot():
    """Public API endpoint to start bot (no auth required)"""
    try:
        if start_bot():
            return jsonify({
                'success': True,
                'message': 'Bot started successfully',
                'bot_running': True
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to start bot',
                'bot_running': False
            })
    except Exception as e:
        logger.error(f"Error in public start bot: {e}")
        return jsonify({
            'success': False,
            'message': 'Error starting bot',
            'bot_running': False
        })

@app.route('/api/public-stop-bot', methods=['POST'])
def public_stop_bot():
    """Public API endpoint to stop bot (no auth required)"""
    try:
        if stop_bot():
            return jsonify({
                'success': True,
                'message': 'Bot stopped successfully',
                'bot_running': False
            })
        else:
            return jsonify({
                'success': False,
                'message': 'Failed to stop bot',
                'bot_running': False
            })
    except Exception as e:
        logger.error(f"Error in public stop bot: {e}")
        return jsonify({
            'success': False,
            'message': 'Error stopping bot',
            'bot_running': False
        })

# Remove the __main__ block since app.py will handle running the Flask app
