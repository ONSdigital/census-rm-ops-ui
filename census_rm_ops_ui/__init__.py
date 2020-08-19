import logging

from flask import Flask
from flask_assets import Environment, Bundle
from structlog import wrap_logger

from census_rm_ops_ui.logger import logger_initial_config
from census_rm_ops_ui.views import setup_blueprints
from config import Config


def create_app():
    app = Flask(__name__)
    assets = Environment(app)
    assets.url = app.static_url_path
    scss_min = Bundle('css/*', 'css/fonts/*', 'css/components/*',
                      filters=['cssmin'], output='minimised/all.min.css')
    assets.register('scss_all', scss_min)
    js_min = Bundle('js/*', filters='jsmin', output='minimised/all.min.js')
    assets.register('js_all', js_min)
    logger_initial_config()
    logger = wrap_logger(logging.getLogger(__name__))
    logger.info('Starting print file service', app_log_level=Config.LOG_LEVEL, pika_log_level=Config.LOG_LEVEL_PIKA,
                paramiko_log_level=Config.LOG_LEVEL_PARAMIKO, environment='DEV')
    setup_blueprints(app)
    return app
