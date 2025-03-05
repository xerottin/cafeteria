import os
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

POSTGRES_URL = os.getenv("POSTGRES_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")
REDIS_CLIENT = os.getenv("REDIS_CLIENT")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
