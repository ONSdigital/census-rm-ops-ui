import os

import jwt
import requests
from flask import request, Blueprint, render_template

IAP_AUDIENCE = os.getenv('IAP_AUDIENCE', None)
home_bp = Blueprint('home_bp', __name__, template_folder='templates', static_folder='static')


def get_jwt():
    if IAP_AUDIENCE:
        try:
            iap_jwt = request.headers['x-goog-iap-jwt-assertion']
            key = get_iap_public_key(jwt.get_unverified_header(iap_jwt).get('kid'))
            decoded_jwt = jwt.decode(iap_jwt, key, algorithms=['ES256'], audience=IAP_AUDIENCE)
            return decoded_jwt
        except KeyError:
            pass

    return {"email": "bananas@noodle.poodle"}


def get_iap_public_key(key_id):
    if key_id not in get_iap_public_key.cache:
        resp = requests.get('https://www.gstatic.com/iap/verify/public_key')
        resp.raise_for_status()
        get_iap_public_key.cache = resp.json()

    return get_iap_public_key.cache[key_id]


get_iap_public_key.cache = {}


@home_bp.route('/')
def index():
    jwt = get_jwt()
    email = jwt['email']
    return render_template('home.html', email=email)

