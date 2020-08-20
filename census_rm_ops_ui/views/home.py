import os

from flask import Blueprint, render_template

IAP_AUDIENCE = os.getenv('IAP_AUDIENCE', None)
home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static')


@home_bp.route('/')
def index():
    return render_template('home.html')
