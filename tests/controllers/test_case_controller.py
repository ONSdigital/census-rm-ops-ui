import json
import urllib
import uuid
from unittest.mock import patch

import pytest
import responses
from requests import HTTPError

from census_rm_ops_ui.controllers.case_controller import get_all_case_details, get_cases_by_postcode, \
    get_qid, get_summary_case_details, submit_qid_link
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

TEST_QID_JSON = {
    'questionnaireId': '987654323456789',
    'caseId': 'Test id'
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
def test_get_case_details_returns_error():
    case_id = str(uuid.uuid4())
    url_safe_case_id = urllib.parse.quote(case_id)

    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/case-details/{url_safe_case_id}',
                  status=500)
    with pytest.raises(HTTPError):
        get_all_case_details(case_id, TestConfig.CASE_API_URL)


@responses.activate
def test_get_qid(app_test_client):
    # Given
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/qids/{TEST_QID_JSON["questionnaireId"]}',
                  json.dumps(TEST_QID_JSON))

    # When
    with app_test_client.app_context():
        qid_response = get_qid(TEST_QID_JSON['questionnaireId'], TestConfig.CASE_API_URL)

    # Then
    unittest_helper.assertEqual(qid_response, TEST_QID_JSON)


@responses.activate
def test_get_qid_404_returned(app_test_client):
    # Given
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/qids/{TEST_QID_JSON["questionnaireId"]}',
                  status=404)

    # When
    with app_test_client.app_context():
        qid_response = get_qid(TEST_QID_JSON['questionnaireId'], TestConfig.CASE_API_URL)

    # Then
    unittest_helper.assertEqual(qid_response, None)


@responses.activate
def test_get_qid_non_404_returned(app_test_client):
    # Given
    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/qids/{TEST_QID_JSON["questionnaireId"]}',
                  status=500)

    # When
    with app_test_client.app_context():
        with pytest.raises(HTTPError):
            get_qid(TEST_QID_JSON['questionnaireId'], TestConfig.CASE_API_URL)


@responses.activate
@patch('uuid.uuid4')
def test_submit_qid_link(patch_uuid, app_test_client):
    # Given
    patch_uuid.return_value = str(uuid.UUID('77f1df52-4b43-11e9-910f-b8ca3a9b9f3e'))
    responses.add(responses.PUT, f'{TestConfig.CASE_API_URL}/qids/link')
    case_id = str(uuid.uuid4())
    expected_payload = {'transactionId': patch_uuid.return_value,
                        'channel': 'ROPS_UI',
                        'qidLink': {"caseId": case_id, "questionnaireId": "987654323456789"}}

    # When
    with app_test_client.app_context():
        qid_response = submit_qid_link(TEST_QID_JSON['questionnaireId'], case_id, TestConfig.CASE_API_URL)

    # Then
    unittest_helper.assertEqual(qid_response.status_code, 200)
    unittest_helper.assertEqual(json.dumps(expected_payload).encode(), qid_response.request.body)


@responses.activate
def test_submit_qid_link_500_error(app_test_client):
    # Given
    responses.add(responses.PUT, f'{TestConfig.CASE_API_URL}/qids/link', status=500)
    case_id = str(uuid.uuid4())

    # When
    with app_test_client.app_context():
        with pytest.raises(HTTPError):
            submit_qid_link(TEST_QID_JSON['questionnaireId'], case_id, TestConfig.CASE_API_URL)


@responses.activate
def test_get_case_summary_success():
    case_id = str(uuid.uuid4())
    url_safe_case_id = urllib.parse.quote(case_id)

    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/{url_safe_case_id}',
                  json.dumps(TEST_CASE))

    case_details = get_summary_case_details(case_id, TestConfig.CASE_API_URL)

    unittest_helper.assertEqual(case_details, TEST_CASE)


@responses.activate
def test_get_case_summary_returns_error():
    case_id = str(uuid.uuid4())
    url_safe_case_id = urllib.parse.quote(case_id)

    responses.add(responses.GET, f'{TestConfig.CASE_API_URL}/cases/{url_safe_case_id}',
                  status=500)
    with pytest.raises(HTTPError):
        get_summary_case_details(case_id, TestConfig.CASE_API_URL)
