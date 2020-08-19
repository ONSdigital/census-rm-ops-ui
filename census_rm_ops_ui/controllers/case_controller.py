import logging

import requests
from requests import HTTPError
from structlog import wrap_logger

from config import Config

logger = wrap_logger(logging.getLogger(__name__))


def get_case_by_postcode(postcode):
    logger.info('Getting case by postcode', postcode=postcode)
    response = requests.get(f'{Config.CASE_API_URL}/cases/postcode', postcode=postcode)
    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            logger.debug('No cases were found for postcode', postcode=postcode)
            return dict()
        logger.debug('Error searching for case by postcode', postcode=postcode)
        raise Exception

    return response.json()
