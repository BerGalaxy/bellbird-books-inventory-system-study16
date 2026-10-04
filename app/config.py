import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY', 'dev-key')
    DEBUG = True