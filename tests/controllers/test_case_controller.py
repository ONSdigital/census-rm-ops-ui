import json
import urllib

import pytest
import responses
from requests import HTTPError

from census_rm_ops_ui.controllers.case_controller import get_cases_by_postcode
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
