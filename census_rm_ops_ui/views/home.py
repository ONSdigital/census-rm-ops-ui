import os

from flask import Blueprint, render_template, request

from census_rm_ops_ui.iap_audit import get_iap_jwt

IAP_AUDIENCE = os.getenv('IAP_AUDIENCE', None)
home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static')


@home_bp.route('/')
def index():
    jwt = get_iap_jwt(request)
    if jwt:
        email = jwt.get('email')
    else:
        email = 'Mr. Test'
    return render_template('home.html', email=email)
