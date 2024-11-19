import os
from dotenv import load_dotenv

load_dotenv()

CREDENTIALS = {
    'SSL_CERT': os.getenv('SSL_CERT_PATH'),
    'SSL_KEY': os.getenv('SSL_KEY_PATH')
}