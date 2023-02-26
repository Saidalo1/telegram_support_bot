import os

from dotenv import load_dotenv

load_dotenv('.env')
TOKEN = os.environ.get('BOT_TOKEN')
OWNER = int(os.environ.get('OWNER_ID'))
DATABASE_USER = os.environ.get('DATABASE_USER')
DATABASE_PASS = os.environ.get('DATABASE_PASS')
DATABASE_HOST = os.environ.get('DATABASE_HOST')
DATABASE_NAME = os.environ.get('DATABASE_NAME')
