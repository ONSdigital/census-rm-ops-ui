from census_rm_ops_ui.views.home import home_bp
from census_rm_ops_ui.views.postcode_search import postcode_search_bp


def setup_blueprints(app):
    app.register_blueprint(postcode_search_bp, url_prefix='/postcode')
    app.register_blueprint(home_bp, url_prefix='/')
    return app