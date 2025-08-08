import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

class Config:
    # Server Configuration
    SERVER_IP = os.getenv('TEST_SERVER_IP')
    if not SERVER_IP:
        raise ValueError("TEST_SERVER_IP environment variable is required. Please set it in your .env file or environment.")
    SERVER_URL = f'http://{SERVER_IP}'
    
    # Database Configuration
    DB_HOST = os.getenv('DB_HOST', SERVER_IP)
    DB_USERNAME = os.getenv('DB_USERNAME')
    DB_PASSWORD = os.getenv('DB_PASSWORD')
    DB_NAME = os.getenv('DB_NAME')
    
    # Validate required database credentials
    if not DB_USERNAME:
        raise ValueError("DB_USERNAME environment variable is required. Please set it in your .env file.")
    if not DB_PASSWORD:
        raise ValueError("DB_PASSWORD environment variable is required. Please set it in your .env file.")
    if not DB_NAME:
        raise ValueError("DB_NAME environment variable is required. Please set it in your .env file.")
    
    # SSH Configuration
    SSH_USERNAME = os.getenv('SSH_USERNAME')
    SSH_PASSWORD = os.getenv('SSH_PASSWORD')
    
    # Validate required SSH credentials
    if not SSH_USERNAME:
        raise ValueError("SSH_USERNAME environment variable is required. Please set it in your .env file.")
    if not SSH_PASSWORD:
        raise ValueError("SSH_PASSWORD environment variable is required. Please set it in your .env file.")
    
    # Test User Credentials
    KWICKPOS_USER = os.getenv('KWICKPOS_USER')
    KWICKPOS_PASS = os.getenv('KWICKPOS_PASS')
    BOSS_USER = os.getenv('BOSS_USER')
    BOSS_PASS = os.getenv('BOSS_PASS')
    
    # Validate required test user credentials
    if not KWICKPOS_USER or not KWICKPOS_PASS:
        raise ValueError("KWICKPOS_USER and KWICKPOS_PASS environment variables are required. Please set them in your .env file.")
    if not BOSS_USER or not BOSS_PASS:
        raise ValueError("BOSS_USER and BOSS_PASS environment variables are required. Please set them in your .env file.")
    
    TEST_USERS = {
        'kwickpos': {
            'username': KWICKPOS_USER,
            'password': KWICKPOS_PASS
        },
        'boss': {
            'username': BOSS_USER,
            'password': BOSS_PASS
        }
    }
    
    # Browser Configuration
    BROWSER = os.getenv('BROWSER', 'chrome')
    HEADLESS = os.getenv('HEADLESS', 'False').lower() == 'true'
    
    # Test Configuration
    IMPLICIT_WAIT = int(os.getenv('IMPLICIT_WAIT', '10'))
    EXPLICIT_WAIT = int(os.getenv('EXPLICIT_WAIT', '20'))