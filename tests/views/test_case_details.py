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


@responses.activate
def test_get_qid_for_linking(app_test_client):
    # Given
    case_id = str(uuid.uuid4())
    qid = '1234567890'

    qid_payload = {
        'caseId': case_id,
        'questionnaireId': qid,
    }

    # Mock the case API response
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/qids/{qid}',
                  body=json.dumps(qid_payload))
    # When
    response = app_test_client.get(f'case-details/questionnaire-id/?qid={qid}&case_id={case_id}')

    # Then
    unittest_helper.assertEqual(response.status_code, 200)
    unittest_helper.assertIn(f'<b>questionnaireId:</b> {qid}'.encode(), response.data)
    unittest_helper.assertIn(f'<b>This QID is already linked to case:</b> {case_id}'.encode(), response.data)
    unittest_helper.assertIn('Link QID'.encode(), response.data)


@responses.activate
def test_get_qid_failed_linking(app_test_client):
    # Given
    case_id = str(uuid.uuid4())
    qid = '1234567890'
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
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/qids/{qid}',
                  status=404)

    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/case-details/{url_safe_case_id}',
                  body=json.dumps(case_details_payload))
    # When
    response = app_test_client.get(f'case-details/questionnaire-id/?qid={qid}&case_id={case_id}', follow_redirects=True)

    # Then
    unittest_helper.assertEqual(response.status_code, 200)
    unittest_helper.assertIn('QID does not exist in RM'.encode(), response.data)


@responses.activate
def test_submitting_qid_link_to_case_api(app_test_client):
    # Given
    case_id = str(uuid.uuid4())
    qid = '1234567890'
    url_safe_case_id = urllib.parse.quote(case_id)

    qid_case_api_payload = {
        'caseId': case_id,
        'questionnaireId': qid,
    }
    request_qid_payload = {
        'case_id': case_id,
        'qid': qid,
    }
    event_payload = json.dumps({"caseId": case_id,
                                "qid": qid})

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
        'events': [{'id': '14063759-c608-4f9f-8fa5-988f52260d7f', 'eventType': 'QUESTIONNAIRE_LINKED',
                    'eventDescription': 'Questionnaire Linked', 'eventDate': '2020-08-26T07:38:47.453158Z',
                    'type': 'None', 'channel': 'RM', 'transactionId': 'None',
                    'eventPayload': event_payload}, ]
    }

    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/case-details/{url_safe_case_id}',
                  body=json.dumps(case_details_payload))

    # Mock the case API response
    responses.add(responses.PUT, f'{TestConfig.CASE_API_URL}/qids/link',
                  json=qid_case_api_payload)
    # When
    response = app_test_client.post('case-details/questionnaire-id/link/', follow_redirects=True,
                                    data=request_qid_payload)

    # Then
    unittest_helper.assertEqual(response.status_code, 200)
    unittest_helper.assertIn('QUESTIONNAIRE_LINKED'.encode(), response.data)
    unittest_helper.assertIn('QID link has been submitted'.encode(), response.data)


def assert_case_details(case_details_payload, response):
    for value in case_details_payload.values():
        if isinstance(value, list):
            for item in value:
                assert_case_details(item, response)
        elif isinstance(value, dict):
            assert_case_details(value, response)
        else:
            unittest_helper.assertIn(value.encode(), response.data)
