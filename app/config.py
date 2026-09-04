"""Application configuration classes for Glitch4ce."""
import os
from datetime import timedelta
from typing import ClassVar

from dotenv import load_dotenv

# Load environment variables from .env if present
basedir = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    """Base configuration."""
    APP_NAME = 'Glitch4ce'
    APP_VERSION = '1.2.0'
    SECRET_KEY = os.environ.get('SECRET_KEY', 'glitch4ce-fallback-dev-secret-key-replace-in-prod')
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16 MB max payload size
    
    # Database
    SQLALCHEMY_DATABASE_URI = os.environ.get(
        'DATABASE_URL',
        f"sqlite:///{os.path.join(basedir, 'game_data.db')}"
    )
    # Fix Render's postgres:// prefix to postgresql:// if needed
    if SQLALCHEMY_DATABASE_URI.startswith('postgres://'):
        SQLALCHEMY_DATABASE_URI = SQLALCHEMY_DATABASE_URI.replace('postgres://', 'postgresql://', 1)
        
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS: ClassVar[dict] = {
        "pool_pre_ping": True,
    }

    # Session & Security
    PERMANENT_SESSION_LIFETIME = timedelta(days=7)
    SESSION_COOKIE_HTTPONLY = True
    SESSION_COOKIE_SAMESITE = 'Lax'
    SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False').lower() in ('true', '1')
    REMEMBER_COOKIE_HTTPONLY = True
    REMEMBER_COOKIE_SECURE = SESSION_COOKIE_SECURE
    REMEMBER_COOKIE_DURATION = timedelta(days=14)
    SECURITY_PASSWORD_SALT = os.environ.get('SECURITY_PASSWORD_SALT', 'glitch4ce-password-salt')

    # Rate Limiting
    RATELIMIT_ENABLED = True
    RATELIMIT_STORAGE_URI = "memory://"
    RATELIMIT_DEFAULT = os.environ.get('RATELIMIT_DEFAULT', '200/hour')
    RATELIMIT_AUTH = os.environ.get('RATELIMIT_AUTH', '20/minute')

    # WTForms / CSRF
    WTF_CSRF_ENABLED = True
    WTF_CSRF_TIME_LIMIT = 3600


class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True
    TESTING = False


class TestingConfig(Config):
    """Testing configuration with in-memory SQLite and disabled CSRF."""
    DEBUG = False
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///:memory:'
    WTF_CSRF_ENABLED = False
    RATELIMIT_ENABLED = False
    SECRET_KEY = 'test-secret-key'


class ProductionConfig(Config):
    """Production configuration."""
    DEBUG = False
    TESTING = False
    SESSION_COOKIE_SECURE = True
    REMEMBER_COOKIE_SECURE = True


config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig,
}

