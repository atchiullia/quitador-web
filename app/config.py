import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or os.urandom(24).hex()
    DEBUG = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
    TEMPLATE_FOLDER = 'app/interface/templates'
    STATIC_FOLDER = 'app/static'

class DevelopmentConfig(Config):
    DEBUG = True

class ProductionConfig(Config):
    DEBUG = False

config = {
    'development': DevelopmentConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
} 