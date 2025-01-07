"""
Configuration settings and constants for the AI Web Search Assistant.
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# API Keys and Endpoints
DEEPSEEK_API_KEY = os.getenv('DEEPSEEK_API_KEY')
BING_API_KEY = os.getenv('BING_API_KEY')
BING_ENDPOINT = os.getenv('BING_ENDPOINT')

# Cache Settings
CACHE_DIR = Path('cache')
CACHE_MAX_AGE_DAYS = 7

# Search Settings
MAX_SEARCH_ROUNDS = 5
RESULTS_PER_SEARCH = 5

# DeepSeek API Settings
DEEPSEEK_BASE_URL = "https://api.deepseek.com"
DEEPSEEK_MODEL = "deepseek-chat"

# Create cache directory if it doesn't exist
CACHE_DIR.mkdir(exist_ok=True) 