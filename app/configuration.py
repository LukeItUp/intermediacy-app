import os

def read_subkey():
    with open('./.sub_key', 'r') as file:
        key = file.read().strip()
    return key

class Config(object):
    DEBUG=True
    APP_DIR = os.path.abspath(os.path.dirname(__file__))  # This directory
    APP_ROOT = os.path.abspath(os.path.join(APP_DIR, os.pardir))
    APP_MEDIA = os.path.os.path.join(APP_DIR, 'media')
    ##URL = os.environ['URL']
    SUB_KEY = read_subkey()

    # Database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_DATABASE_URI = 'postgresql+psycopg2://postgres@db:5432/postgres'

    # Worker
    CELERY_BROKER_URL = 'redis://redis:6379/0'
    CELERY_RESULT_BACKEND = 'redis://redis:6379/0'
