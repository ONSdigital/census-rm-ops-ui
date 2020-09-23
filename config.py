import os


class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%Y-%m-%dT%H:%M:%S.%f')

    CASE_API_URL = os.getenv('CASE_API_URL')

    IAP_AUDIENCE = os.getenv('IAP_AUDIENCE')

    ENVIRONMENT = os.getenv('ENVIRONMENT')

    OPS_UI_SECRET = os.getenv('OPS_UI_SECRET')

    PREFERRED_URL_SCHEME = 'https'

    IN_GCP = os.getenv('IN_GCP', False)


class DevelopmentConfig(Config):
    DEBUG = os.getenv('DEBUG')
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'DEBUG')
    CASE_API_URL = os.getenv('CASE_API_URL', 'http://localhost:8161')
    ENVIRONMENT = os.getenv('ENVIRONMENT', 'DEV')
    OPS_UI_SECRET = os.getenv('OPS_UI_SECRET', 'secret')
    PREFERRED_URL_SCHEME = 'http'


class TestConfig(DevelopmentConfig):
    # Dummy URL to avoid any real API calls going out
    CASE_API_URL = 'http://test'

    ENVIRONMENT = 'TEST'
    TESTING = True
