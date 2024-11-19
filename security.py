import os
from fastapi.security import OAuth2PasswordBearer
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")
from passlib.context import CryptContext
from dotenv import load_dotenv

load_dotenv()

# to get a string like this run:
# openssl rand -hex 32

SECRET_KEY = os.getenv('SECRET_KEY')
ALGORITHM = os.getenv('ALGORITHM')
ACCESS_TOKEN_EXPIRE_MINUTES = os.getenv('ACCESS_TOKEN_EXPIRE_MINUTES')

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

