import logging

import requests
from flask import current_app
from requests import HTTPError
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def get_case_by_postcode(postcode):
    logger.debug('Getting case by postcode', postcode=postcode)
    response = requests.get(f'{current_app.config["CASE_API_URL"]}/cases/postcode/{postcode}')
    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            logger.debug('No cases were found for postcode', postcode=postcode)
            return dict()
        logger.debug('Error searching for case by postcode', postcode=postcode)
        raise

    return response.json()
