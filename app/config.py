import os
from dotenv import load_dotenv

#Load_environment_variables_from_.env_file
load_dotenv()

class Config:
    """Base configuration."""
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'you-will-never-guess'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    UPLOAD_FOLDER = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'static', 'uploads')
    ALLOWED_EXTENSIONS = {'pdf', 'jpeg', 'jpg', 'png'}

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    db_user = os.environ.get('DATABASE_USER')
    db_pass = os.environ.get('DATABASE_PASSWORD')
    db_host = os.environ.get('DATABASE_HOST')
    db_port = os.environ.get('DATABASE_PORT')
    db_name = os.environ.get('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'  # Use in-memory SQLite for tests
    WTF_CSRF_ENABLED = False
    SERVER_NAME = 'localhost'

class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    db_user = os.environ.get('DATABASE_USER')
    db_pass = os.environ.get('DATABASE_PASSWORD')
    db_host = os.environ.get('DATABASE_HOST')
    db_port = os.environ.get('DATABASE_PORT')
    db_name = os.environ.get('DATABASE_NAME')
    SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://{db_user}:{db_pass}@{db_host}:{db_port}/{db_name}"


config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
