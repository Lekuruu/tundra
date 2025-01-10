
import dotenv
import os

dotenv.load_dotenv(override=False)

POSTGRES_HOST = os.environ.get('POSTGRES_HOST', 'localhost')
POSTGRES_PORT = int(os.environ.get('POSTGRES_PORT', '5432'))
POSTGRES_DBNAME = os.environ.get('POSTGRES_DBNAME', 'postgres')
POSTGRES_USER = os.environ.get('POSTGRES_USER', 'postgres')
POSTGRES_PASSWORD = os.environ.get('POSTGRES_PASSWORD')

WEB_HOST = os.environ.get('WEB_HOST')
WEB_PORT = int(os.environ.get('WEB_PORT', 80))
WEB_DOMAIN = os.environ.get('WEB_DOMAIN', 'localhost')
WEB_TOKEN_EXPIRATION = int(os.environ.get('WEB_TOKEN_EXPIRATION', '3600'))

SSL_ENABLED = os.environ.get('SSL_ENABLED', 'false').lower() == 'true'
SSL_KEY_PATH = os.environ.get('SSL_KEY_PATH')
SSL_CERT_PATH = os.environ.get('SSL_CERT_PATH')

SITE_NAME = os.environ.get('SITE_NAME', 'localhost')
FROM_EMAIL = os.environ.get('FROM_EMAIL', 'noreply@localhost')
SENDGRID_API_KEY = os.environ.get('SENDGRID_API_KEY', '')
MAX_ACCOUNT_EMAIL = int(os.environ.get('MAX_ACCOUNT_EMAIL', '5'))
STATIC_KEY = os.environ.get('STATIC_KEY', 'houdini')

USERNAME_FORCE_CASE = os.environ.get('USERNAME_FORCE_CASE', 'false').lower() == 'true'
APPROVE_USERNAME = os.environ.get('APPROVE_USERNAME', 'false').lower() == 'true'
ACTIVATE_PLAYER = os.environ.get('ACTIVATE_PLAYER', 'false').lower() == 'true'
DEBUG = os.environ.get('DEBUG', 'false').lower() == 'true'
RELOAD = os.environ.get('RELOAD', str(DEBUG)).lower() == 'true'

PROTOCOL = 'https' if SSL_ENABLED else 'http'
HOME_BASEURL = os.environ.get('HOME_BASEURL', f'{PROTOCOL}://{WEB_DOMAIN}')
PLAY_BASEURL = os.environ.get('PLAY_BASEURL', f'{PROTOCOL}://play.{WEB_DOMAIN}')
API_BASEURL = os.environ.get('API_BASEURL', f'{PROTOCOL}://api.{WEB_DOMAIN}')
MEDIA1_BASEURL = os.environ.get('MEDIA1_BASEURL', f'{PROTOCOL}://media.{WEB_DOMAIN}')
MEDIA8_BASEURL = os.environ.get('MEDIA8_BASEURL', f'{PROTOCOL}://media.{WEB_DOMAIN}')
WNS_URL = os.environ.get('WNS_URL', f'{PROTOCOL}://n7vcp1clubpwns.{WEB_DOMAIN}')
