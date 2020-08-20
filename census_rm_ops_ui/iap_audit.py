import logging
from functools import lru_cache

import jwt
import requests
from flask import request
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def log_iap_audit(iap_audience):
    iap_jwt = get_iap_jwt(iap_audience) if iap_audience else {'email': 'TEST'}
    if not iap_jwt:
        return
    logger.info(audit=True,
                requestPath=request.full_path,
                requestMethod=request.method,
                user=iap_jwt["email"])


def get_iap_jwt(iap_audience):
    iap_jwt = request.headers.get('x-goog-iap-jwt-assertion')
    if not iap_jwt:
        return
    key = get_iap_public_key(jwt.get_unverified_header(iap_jwt).get('kid'))
    # Note ES256 requires the cryptography module
    decoded_jwt = jwt.decode(iap_jwt, key, algorithms=['ES256'], audience=iap_audience)
    return decoded_jwt


@lru_cache()
def get_iap_public_key(key_id):
    resp = requests.get('https://www.gstatic.com/iap/verify/public_key')
    resp.raise_for_status()
    iap_public_key_cache = resp.json()
    return iap_public_key_cache[key_id]
