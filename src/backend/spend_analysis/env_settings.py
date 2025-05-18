import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables from .env file
env_path = Path(__file__).resolve().parent.parent.parent / '.env'
load_dotenv(env_path)

def get_env_variable(var_name, default=None):
    """Get the environment variable or return default value"""
    return os.getenv(var_name, default)

# Environment-based settings
DEBUG = get_env_variable('DEBUG', 'True') == 'True'
SECRET_KEY = get_env_variable('SECRET_KEY', 'django-insecure-default-key-for-development')
ALLOWED_HOSTS = get_env_variable('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Database settings
DB_ENGINE = get_env_variable('DB_ENGINE', 'django.db.backends.sqlite3')
DB_NAME = get_env_variable('DB_NAME', 'db.sqlite3')
DB_USER = get_env_variable('DB_USER', '')
DB_PASSWORD = get_env_variable('DB_PASSWORD', '')
DB_HOST = get_env_variable('DB_HOST', '')
DB_PORT = get_env_variable('DB_PORT', '')

# CORS settings
CORS_ALLOW_ALL_ORIGINS = get_env_variable('CORS_ALLOW_ALL_ORIGINS', 'True') == 'True'
CORS_ALLOWED_ORIGINS = get_env_variable('CORS_ALLOWED_ORIGINS', '').split(',') if get_env_variable('CORS_ALLOWED_ORIGINS') else []

# Frontend URL for redirects
FRONTEND_URL = get_env_variable('FRONTEND_URL', 'http://localhost:3000')