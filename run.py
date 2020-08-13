from flask import Flask, request
import jwt
import requests
import os

app = Flask(__name__)

IAP_AUDIENCE = os.getenv('IAP_AUDIENCE', None)


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


@app.route('/')
def index():
    jwt = get_jwt()
    return f"Hello World... I think your email is: {jwt['email']} ...here is everything I know about you: {jwt}"


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=os.getenv('PORT', '8234'))
