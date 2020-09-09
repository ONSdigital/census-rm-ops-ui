import logging
import os
from functools import partial

from flask import Flask
from flask_assets import Environment
from structlog import wrap_logger
from webassets import Bundle
from werkzeug.middleware.proxy_fix import ProxyFix

from census_rm_ops_ui.iap_audit import log_iap_audit
from census_rm_ops_ui.logger import logger_initial_config
from census_rm_ops_ui.views import setup_blueprints


def create_app(config_name='Config'):
    app = Flask(__name__)
    config_name = os.getenv('APP_SETTINGS', config_name)
    app.config.from_object(f'config.{config_name}')
    # Set the secret key to some random bytes. Keep this really secret!
    app.secret_key = app.config.get('OPS_UI_SECRET')
    if app.config['IN_GCP'] == 'true':
        app.wsgi_app = ProxyFix(app.wsgi_app)
    logger_initial_config()
    logger = wrap_logger(logging.getLogger(__name__))
    logger.info('Starting Census Response Operations UI',
                app_log_level=app.config['LOG_LEVEL'],
                environment=app.config['ENVIRONMENT'])

    assets = Environment(app)
    assets.url = app.static_url_path
    scss_min = Bundle('css/*', 'css/fonts/*', 'css/components/*',
                      filters=['cssmin'], output='minimised/all.min.css')
    assets.register('scss_all', scss_min)
    js_min = Bundle('js/*', filters='jsmin', output='minimised/all.min.js')
    assets.register('js_all', js_min)

    app.before_request(partial(log_iap_audit, iap_audience=app.config['IAP_AUDIENCE']))

    setup_blueprints(app)

    return app
