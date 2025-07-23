import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Config:
    """Configuration class for the application"""
    
    # Flask Configuration
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-change-in-production'
    DEBUG = os.environ.get('DEBUG', 'True').lower() == 'true'
    
    # AI Model Configuration
    OPENAI_API_KEY = os.environ.get('OPENAI_API_KEY')
    DEFAULT_MODEL = os.environ.get('DEFAULT_MODEL', 't5-base')
    
    # Feature Flags
    ENABLE_CODE_ANALYSIS = os.environ.get('ENABLE_CODE_ANALYSIS', 'True').lower() == 'true'
    ENABLE_SECURITY_SCAN = os.environ.get('ENABLE_SECURITY_SCAN', 'True').lower() == 'true'
    ENABLE_PERFORMANCE_ANALYSIS = os.environ.get('ENABLE_PERFORMANCE_ANALYSIS', 'True').lower() == 'true'
    
    # File Upload Configuration
    MAX_CONTENT_LENGTH = 16 * 1024 * 1024  # 16MB max file size
    ALLOWED_EXTENSIONS = {'py', 'js', 'java', 'cpp', 'c', 'ts', 'jsx', 'tsx', 'php', 'rb', 'go', 'rs', 'swift'}
    
    # Rate Limiting
    MAX_REQUESTS_PER_MINUTE = int(os.environ.get('MAX_REQUESTS_PER_MINUTE', '30'))
    
    # Database Configuration (for future use)
    DATABASE_URL = os.environ.get('DATABASE_URL')
