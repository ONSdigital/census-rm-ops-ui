import json
import urllib

import responses

from census_rm_ops_ui.views.postcode_search import ADDRESS_SUMMARY_FIELDS
from config import TestConfig
from tests import unittest_helper


def test_postcode_search(app_test_client):
    # When
    response = app_test_client.get('/')

    # Then
    unittest_helper.assertEqual(response.status_code, 200)
    unittest_helper.assertIn(b'Census ROps Case Management', response.data)
    unittest_helper.assertIn(b'Search cases', response.data)
    unittest_helper.assertIn(b'Enter a postcode', response.data)


@responses.activate
def test_postcode_search_results(app_test_client):
    # Given
    postcode = 'AB1 2CD'
    url_safe_postcode = urllib.parse.quote(postcode)
    case = {
        'organisationName': 'test_org',
        'addressLine1': 'Somewhere',
        'addressLine2': 'Over The',
        'addressLine3': 'Rainbow',
        'townName': 'Newport',
        'postcode': postcode,
        'caseType': 'HH',
        'addressLevel': 'U',
        'estabType': 'HOUSEHOLD',
        'caseRef': '123456789'
    }

    # Mock the case API response
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/postcode/{url_safe_postcode}',
                  body=json.dumps([case]))

    # When
    response = app_test_client.get(f'/postcode/?postcode={url_safe_postcode}')

    # Then
    unittest_helper.assertEqual(response.status_code, 200)
    unittest_helper.assertIn(f'1 result for postcode: "{postcode}"'.encode(), response.data)

    # Check the address summary line is there
    unittest_helper.assertIn(
        ', '.join([v for k, v in case.items() if k in ADDRESS_SUMMARY_FIELDS]).encode(),
        response.data)
    for value in case.values():
        unittest_helper.assertIn(value.encode(), response.data)


@responses.activate
def test_postcode_search_no_results(app_test_client):
    # Given
    no_matches_postcode = 'test'

    # Mock the case API response
    responses.add(responses.GET,
                  f'{TestConfig.CASE_API_URL}/cases/postcode/{no_matches_postcode}',
                  status=404)

    # When
    response = app_test_client.get(f'/postcode/?postcode={no_matches_postcode}')

    # Then
    unittest_helper.assertEqual(response.status_code, 200)
    unittest_helper.assertIn(f'0 results for postcode: "{no_matches_postcode}"'.encode(), response.data)
