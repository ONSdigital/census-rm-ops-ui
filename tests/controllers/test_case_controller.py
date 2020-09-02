import json
import urllib
import uuid

import pytest
import responses
from requests import HTTPError

from census_rm_ops_ui.controllers.case_controller import get_cases_by_postcode, get_all_case_details
from config import TestConfig
from tests import unittest_helper

TEST_CASE = {
    'organisationName': 'test_org',
    'addressLine1': 'Somewhere',
    'addressLine2': 'Over The',
    'addressLine3': 'Rainbow',
    'townName': 'Newport',
    'postcode': 'AB1 2CD',
    'caseType': 'HH',
    'addressLevel': 'U',
    'estabType': 'HOUSEHOLD',
    'caseRef': '123456789'
}


@responses.activate
def test_get_cases_by_postcode_success():
    # Given
    url_safe_postcode = urllib.parse.quote(TEST_CASE['postcode'])
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/postcode/{url_safe_postcode}',
                  json.dumps([TEST_CASE]))

    # When
    cases = get_cases_by_postcode(TEST_CASE['postcode'], TestConfig.CASE_API_URL)

    # Then
    unittest_helper.assertEqual(cases, [TEST_CASE])


@responses.activate
def test_get_cases_by_postcode_no_matches():
    # Given
    url_safe_postcode = urllib.parse.quote(TEST_CASE['postcode'])
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/postcode/{url_safe_postcode}',
                  status=404)

    # When
    cases = get_cases_by_postcode(TEST_CASE['postcode'], TestConfig.CASE_API_URL)

    # Then
    unittest_helper.assertEqual(cases, dict())


@responses.activate
def test_get_cases_by_postcode_raises_non_404_errors():
    # Given
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/postcode/test',
                  status=500)

    # When, then raises
    with pytest.raises(HTTPError):
        get_cases_by_postcode('test', TestConfig.CASE_API_URL)


@responses.activate
def test_get_case_details_success():
    case_id = str(uuid.uuid4())
    url_safe_case_id = urllib.parse.quote(case_id)

    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/case-details/{url_safe_case_id}',
                  json.dumps(TEST_CASE))

    case_details = get_all_case_details(case_id, TestConfig.CASE_API_URL)

    unittest_helper.assertEqual(case_details, TEST_CASE)


@responses.activate
def test_get_case_details_returnss_error():
    case_id = str(uuid.uuid4())
    url_safe_case_id = urllib.parse.quote(case_id)

    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/case-details/{url_safe_case_id}',
                  status=500)
    with pytest.raises(HTTPError):
        get_all_case_details(case_id, TestConfig.CASE_API_URL)
