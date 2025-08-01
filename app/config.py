import os

# Base-Config (shared by every environment)
class Config:
    DEBUG = False  # Default: overridden by child classes
    SECRET_KEY = os.environ.get("SECRET_KEY")
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")

    # Compose DB URI from env variables
    DB_USER = os.environ.get("DB_USER")
    DB_PASSWORD = os.environ.get("DB_PASSWORD")
    DB_HOST = os.environ.get("DB_HOST")
    DB_PORT = os.environ.get("DB_PORT", "3306")
    DB_NAME = os.environ.get("DB_NAME")

    SQLALCHEMY_DATABASE_URI = (
        f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Logging Configuration
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'logs', 'app.log')
    LOG_LEVEL = 'DEBUG'  # Can be overridden in Production if needed

# Development-specific settings
class DevelopmentConfig(Config):
    DEBUG = True

# Production-specific settings
class ProductionConfig(Config):
    DEBUG = False
    LOG_LEVEL = 'ERROR'  # Optional: for less verbose logging in production

# Testing-specific settings
class TestingConfig(Config):
    TESTING = True  # ✅ This was `Testing` (capital T), should be `TESTING` to work with Flask
