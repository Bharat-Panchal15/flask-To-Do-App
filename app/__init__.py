from flask import Flask, render_template, request, redirect, url_for
from flask_jwt_extended import JWTManager
from dotenv import load_dotenv
from app.extensions import db
import os
import logging

jwt = JWTManager()

def create_app(config_class='app.config.DevelopmentConfig'):
    app = Flask(__name__)
    load_dotenv()

    # Loads settings like SECRET_KEY, DEBUG, database URI,etc.
    app.config.from_object(config_class)

    # Setup logging
    log_file = app.config.get('LOG_FILE')
    log_level = app.config.get('LOG_LEVEL').upper()

    # Make sure logging folder exists
    os.makedirs(os.path.dirname(log_file),exist_ok=True)

    # Configure logging
    level = getattr(logging,log_level,logging.DEBUG)
    logging.basicConfig(filename=log_file,level=level,format="%(asctime)s [%(levelname)s] %(message)s")

    # Initialize extensions (like SQLAlchemy)
    db.init_app(app)
    jwt.init_app(app)

    # Import blueprints
    from app.auth import auth_bp
    from app.dashboard import dashboard_bp
    from app.api import api_bp

    from app import models

    # Attaches blueprints
    app.register_blueprint(auth_bp, url_prefix='/auth')
    app.register_blueprint(dashboard_bp, url_prefix='/dashboard')
    app.register_blueprint(api_bp, url_prefix='/api')

    @app.route('/')
    def home():
        return redirect(url_for('auth.register'))

    @app.errorhandler(404)
    def not_found_error(error):
        logging.error(f"404 Error: {request.path}")
        return render_template('404.html'),404
    
    @app.errorhandler(500)
    def internal_error(error):
        logging.error(f"500 Error: {request.path}")
        return render_template('500.html'),500

    return app