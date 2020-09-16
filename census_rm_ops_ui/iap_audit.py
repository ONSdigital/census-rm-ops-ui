import logging
from functools import lru_cache

import jwt
import requests
from flask import request, g
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def log_iap_audit(iap_audience):
    iap_jwt = get_iap_jwt(iap_audience) if iap_audience else {'email': 'TEST'}
    g.user = iap_jwt['email']
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
    # Get the signing key ID from the header
    key = get_iap_public_key(jwt.get_unverified_header(iap_jwt).get('kid'))

    # Note ES256 requires the cryptography module
    decoded_jwt = jwt.decode(iap_jwt, key, algorithms=['ES256'], audience=iap_audience)
    return decoded_jwt


def get_iap_public_key(key_id):
    try:
        return get_iap_public_keys()[key_id]
    except KeyError:
        # Try refreshing the public keys if the key ID is not in the cache
        get_iap_public_keys.cache_clear()
        refreshed_public_keys = get_iap_public_keys()
        return refreshed_public_keys[key_id]


@lru_cache()
def get_iap_public_keys():
    resp = requests.get('https://www.gstatic.com/iap/verify/public_key')
    resp.raise_for_status()
    return resp.json()
