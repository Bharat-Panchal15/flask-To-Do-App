import os

# Base-Config (shared by every environment)
class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False # True for development/ False for production
    JWT_SECRET_KEY = os.getenv("JWT_SECRET_KEY")

    # Logging Configuration
    LOG_FILE = os.path.join(os.path.dirname(os.path.dirname(__file__)),'logs','app.log')
    LOG_LEVEL = 'DEBUG' # DEBUG, INFO , WARNING, ERROR, CRITICAL

# Development-specific settings
class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

# Production-specific settings
class ProductionConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = os.getenv("DATABASE_URL",f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}")
    SQLALCHEMY_TRACK_MODIFICATIONS = False

class TestingConfig(Config):
    Testing = True
    SQLALCHEMY_DATABASE_URI = f"mysql+pymysql://{os.getenv('DB_USER')}:{os.getenv('DB_PASSWORD')}@{os.getenv('DB_HOST')}/{os.getenv('DB_NAME')}" # In-memory DB for speed
    SQLALCHEMY_TRACK_MODIFICATIONS = False