
import dotenv
import os

dotenv.load_dotenv(override=True)

WEB_HOST = os.environ.get('WEB_HOST')
WEB_PORT = int(os.environ.get('WEB_PORT', 80))

DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
