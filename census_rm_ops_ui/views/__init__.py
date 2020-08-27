from census_rm_ops_ui.views.case_details import case_details_bp
from census_rm_ops_ui.views.postcode_search import postcode_search_bp
from census_rm_ops_ui.views.health import health_bp


def setup_blueprints(app):
    app.register_blueprint(postcode_search_bp, url_prefix='/')
    app.register_blueprint(health_bp, url_prefix='/health')
    app.register_blueprint(case_details_bp, url_prefix='/case_details')
    return app
