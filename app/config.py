import os

from dotenv import load_dotenv

load_dotenv()

# .env globals
APP_SECRET = os.environ.get("APP_SECRET")
CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")
AUTHORIZATION_URL = os.environ.get("AUTHORIZATION_URL")
TOKEN_URL = os.environ.get("TOKEN_URL")
API_BASE_URL = os.environ.get("API_BASE_URL")

# Other globals
SCOPE = "user-read-private user-read-email"
