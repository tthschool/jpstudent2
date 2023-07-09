import os
from dotenv import load_dotenv

# Load các biến môi trường từ tệp .env
load_dotenv()

SQLALCHEMY_DATABASE_URI = os.environ.get('DATABASE_URL')
SECRET_KEY = os.environ.get('SECRET_KEY')
SQLALCHEMY_TRACK_MODIFICATIONS = False
