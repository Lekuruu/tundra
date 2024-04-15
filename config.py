
import dotenv
import os

dotenv.load_dotenv(override=True)

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', '5432'))
POSTGRES_DBNAME = os.environ.get('POSTGRES_DBNAME', 'postgres')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

WEB_HOST = os.environ.get('WEB_HOST')
WEB_PORT = int(os.environ.get('WEB_PORT', 80))

DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
