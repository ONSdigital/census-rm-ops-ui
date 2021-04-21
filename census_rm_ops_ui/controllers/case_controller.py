import logging
import urllib
import uuid

import requests
from flask import g
from requests import HTTPError
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))


def get_cases_by_postcode(postcode, case_api_url):
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


def get_all_case_details(case_id, case_api_url):
    logger.debug('Getting all case details', case_id=case_id)
    response = requests.get(f'{case_api_url}/cases/case-details/{urllib.parse.quote(case_id)}')
    try:
        response.raise_for_status()
    except HTTPError:
        logger.error('Error searching for details of case', case_id=case_id)
        raise

    return response.json()


def get_summary_case_details(case_id, case_api_url):
    logger.debug('Getting all case details', case_id=case_id)
    response = requests.get(f'{case_api_url}/cases/{urllib.parse.quote(case_id)}')
    try:
        response.raise_for_status()
    except HTTPError:
        logger.error('Error searching for summary details of case', case_id=case_id)
        raise

    return response.json()


def get_qid(qid, case_api_url):
    logger.debug('Getting qid details', qid=qid, user=g.get('user'))
    response = requests.get(f'{case_api_url}/qids/{urllib.parse.quote(qid)}')
    try:
        response.raise_for_status()
    except HTTPError:
        if response.status_code == 404:
            return None
        logger.error('Error searching for qid', qid=qid, user=g.get('user'))
        raise

    return response.json()


def submit_qid_link(qid, case_id, case_api_url):
    tx_id = str(uuid.uuid4())
    logger.info('Attempting to submit qid link', qid=qid, case_id=case_id, user=g.get('user'), tx_id=tx_id, audit=True)
    payload = {'transactionId': tx_id,
               'channel': 'ROPS_UI',
               'qidLink': {'caseId': case_id, 'questionnaireId': qid}}
    response = requests.put(f'{case_api_url}/qids/link', json=payload)
    try:
        response.raise_for_status()
    except HTTPError:
        logger.error('Error attempting to submit qid link', case_id=case_id, qid=qid, user=g.get('user'), tx_id=tx_id,
                     audit=True)
        raise

    return response
