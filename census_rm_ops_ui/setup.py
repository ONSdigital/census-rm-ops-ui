import logging
import os

from flask import Flask
from flask_assets import Environment
from structlog import wrap_logger
from webassets import Bundle

from census_rm_ops_ui.iap_audit import log_iap_audit
from census_rm_ops_ui.logger import logger_initial_config
from census_rm_ops_ui.views import setup_blueprints
from config import Config


def create_app(config_name='Config'):
    app = Flask(__name__)
    config_name = os.getenv('APP_SETTINGS', config_name)
    app.config.from_object(f'config.{config_name}')

    logger_initial_config()
    logger = wrap_logger(logging.getLogger(__name__))
    # TODO
    logger.info('Starting print file service', app_log_level=Config.LOG_LEVEL, environment='DEV')

    assets = Environment(app)
    assets.url = app.static_url_path
    scss_min = Bundle('css/*', 'css/fonts/*', 'css/components/*',
                      filters=['cssmin'], output='minimised/all.min.css')
    assets.register('scss_all', scss_min)
    js_min = Bundle('js/*', filters='jsmin', output='minimised/all.min.js')
    assets.register('js_all', js_min)

    app.before_request(log_iap_audit)
    setup_blueprints(app)

    return app
