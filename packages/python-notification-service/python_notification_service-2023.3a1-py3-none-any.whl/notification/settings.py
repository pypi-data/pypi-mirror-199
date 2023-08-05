import os

from dotenv import load_dotenv

load_dotenv()

env = os.getenv

# Define list of fixed parameters or constants

APP_NAME = env('APP_NAME')

# AWS Settings
AWS_ACCESS_KEY = env('AWS_ACCESS_KEY')
AWS_SECRET_ACCESS_KEY = env('AWS_SECRET_ACCESS_KEY')
AWS_REGION = env('AWS_REGION')

ZEPTO_EMAIL_API = 'https://api.zeptomail.com/v1.1/email/template'
MAILGUN_EMAIL_API = ''
