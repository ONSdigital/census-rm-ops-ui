import os


class Config:
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    LOG_DATE_FORMAT = os.getenv('LOG_DATE_FORMAT', '%Y-%m-%dT%H:%M:%S.%f')
    LOG_LEVEL_PIKA = os.getenv('LOG_LEVEL_PIKA', 'ERROR')
    LOG_LEVEL_PARAMIKO = os.getenv('LOG_LEVEL_PARAMIKO', 'ERROR')

    CASE_API_URL = os.getenv('CASE_API_URL', 'http://localhost:8161')

    IAP_AUDIENCE = os.getenv('IAP_AUDIENCE', None)
