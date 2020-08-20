import logging
import urllib

import requests
from requests import HTTPError
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def get_case_by_postcode(postcode, case_api_url):
    logger.debug('Getting case by postcode', postcode=postcode)
    response = requests.get(f'{case_api_url}/cases/postcode/{urllib.parse.quote(postcode)}')
    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            logger.debug('No cases were found for postcode', postcode=postcode)
            return dict()
        logger.error('Error searching for case by postcode', postcode=postcode)
        raise

    return response.json()
