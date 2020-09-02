import json
import urllib
import uuid

import responses

from config import TestConfig
from tests import unittest_helper


@responses.activate
def test_case_details_results(app_test_client):
    # Given
    case_id = str(uuid.uuid4())
    url_safe_case_id = urllib.parse.quote(case_id)

    case_details_payload = {
        'id': case_id,
        'organisationName': 'test_org',
        'addressLine1': 'Somewhere',
        'addressLine2': 'Over The',
        'addressLine3': 'Rainbow',
        'townName': 'Newport',
        'postcode': 'XX0 0XX',
        'caseType': 'HH',
        'addressLevel': 'U',
        'estabType': 'HOUSEHOLD',
        'caseRef': '123456789',
        'events': [{'id': '14063759-c608-4f9f-8fa5-988f52260d7f', 'eventType': 'SAMPLE_LOADED',
                    'eventDescription': 'Create case sample received', 'eventDate': '2020-08-26T07:38:47.453158Z',
                    'type': 'None', 'channel': 'RM', 'transactionId': 'None',
                    'eventPayload': '{\"testKey\": \"testValue\"}'}, ]
    }
    # Mock the case API response
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/case-details/{url_safe_case_id}',
                  body=json.dumps(case_details_payload))
    # When
    response = app_test_client.get(f'/case-details/?case_id={url_safe_case_id}')

    # Then

    case_details_payload['events'][0]['eventPayload'] = json.loads(case_details_payload['events'][0]['eventPayload'])

    unittest_helper.assertEqual(response.status_code, 200)
    assert_case_details(case_details_payload, response)


def assert_case_details(case_details_payload, response):
    for value in case_details_payload.values():
        if isinstance(value, list):
            for item in value:
                assert_case_details(item, response)
        elif isinstance(value, dict):
            assert_case_details(value, response)
        else:
            unittest_helper.assertIn(value.encode(), response.data)
