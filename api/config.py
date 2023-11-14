import os
from dotenv import load_dotenv

load_dotenv()

postgres_local_base = os.environ['DATABASE_URL']


class Config:
    DEBUG = False


class DevConfig(Config): # will use cloud instance of a database
    SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = None
    

class ProdConfig(Config):
    DEBUG = False
    SQLALCHEMY_DATABASE_URI = None


config_by_name = {
    'dev': DevConfig,
    'prod': ProdConfig,
    'test': TestConfig
}

