import os

ELK_URL = os.getenv('ELK_URL', 'https://elastic.sysnet.cz:443')
ELK_USERNAME = os.getenv('ELK_USERNAME', None)
ELK_PASSWORD = os.getenv('ELK_PASSWORD', None)
ELK_CERTS_DIR = os.getenv('ELK_CERTS_DIR', 'certs')
ELK_CERTS_CA = ''
if ELK_CERTS_DIR != '':
    ELK_CERTS_CA = os.path.join(ELK_CERTS_DIR, 'ca', 'ca.pem')
ELK_VERIFY_CERTS = os.getenv("ELK_VERIFY_CERTS", 'False').lower() in ('true', '1', 't')

TWITTER_CONSUMER_KEY = os.getenv('TWITTER_CONSUMER_KEY', None)
TWITTER_CONSUMER_SECRET = os.getenv('TWITTER_CONSUMER_SECRET', None)
TWITTER_ACCESS_TOKEN = os.getenv('TWITTER_ACCESS_TOKEN', None)
TWITTER_ACCESS_TOKEN_SECRET = os.getenv('TWITTER_ACCESS_TOKEN_SECRET', None)
TWITTER_BEARER_TOKEN = os.getenv('TWITTER_BEARER_TOKEN', None)

RUIAN_API = os.getenv('RUIAN_API', None)
RUIAN_HOST = os.getenv('RUIAN_HOST', 'https://service.sysnet.cz/SYSNET/RUIAN/1.0.2')


class ShoppingError(Exception):
    pass
