import os
from dotenv import load_dotenv

load_dotenv()

# All environment variables loaded in one place
SECRET_KEY = os.getenv("SECRET_KEY", "bytebites-dev-secret")
