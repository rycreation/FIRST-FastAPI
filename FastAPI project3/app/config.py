from dotenv import load_dotenv
import os

# Load environment variables from .env
load_dotenv()

# Database URL
DATABASE_URL = os.getenv("DATABASE_URL")

# JWT Secret Key
SECRET_KEY = os.getenv("SECRET_KEY")

# JWT Algorithm
ALGORITHM = os.getenv("ALGORITHM", "HS256")

# Access token expiry (minutes)
ACCESS_TOKEN_EXPIRE_MINUTES = int(
    os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30)
)