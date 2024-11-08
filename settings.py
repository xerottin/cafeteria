import os
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())

DATABASE_URL = os.getenv("DATABASE_URL")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
USERNAME = os.getenv("USERNAME")
PASSWORD = os.getenv("PASSWORD")

ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))
