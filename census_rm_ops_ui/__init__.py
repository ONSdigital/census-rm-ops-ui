import logging

from flask import Flask
from structlog import wrap_logger

from census_rm_ops_ui.logger import logger_initial_config
from census_rm_ops_ui.views import setup_blueprints
from config import Config


def create_app():
    app = Flask(__name__)
    logger_initial_config()
    logger = wrap_logger(logging.getLogger(__name__))
    logger.info('Starting print file service', app_log_level=Config.LOG_LEVEL, pika_log_level=Config.LOG_LEVEL_PIKA,
                paramiko_log_level=Config.LOG_LEVEL_PARAMIKO, environment='DEV')
    setup_blueprints(app)
    return app
