import logging
from functools import lru_cache

import jwt
import requests
from flask import current_app, request
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def log_iap_audit():
    # iap_jwt = get_iap_jwt(request)
    # TODO undo this unholy abomination
    iap_jwt = {'email': 'banana'}
    if not iap_jwt:
        return
    logger.info(audit=True,
                requestPath=request.path,
                requestMethod=request.method,
                user=iap_jwt["email"])


def get_iap_jwt(request):
    iap_jwt = request.headers.get('x-goog-iap-jwt-assertion')
    if not iap_jwt:
        return
    key = get_iap_public_key(jwt.get_unverified_header(iap_jwt).get('kid'))
    decoded_jwt = jwt.decode(iap_jwt, key, algorithms=['ES256'], audience=current_app.config.IAP_AUDIENCE)
    return decoded_jwt


@lru_cache()
def get_iap_public_key(key_id):
    resp = requests.get('https://www.gstatic.com/iap/verify/public_key')
    resp.raise_for_status()
    iap_public_key_cache = resp.json()
    return iap_public_key_cache[key_id]
