from unittest.mock import Mock, patch

import requests

from census_rm_ops_ui.iap_audit import get_iap_public_key


@patch('census_rm_ops_ui.iap_audit.requests')
def test_get_iap_public_key(patched_requests):
    # Given
    test_id = 'test_id'
    dummy_key = 'dummy_key'
    mock_response = Mock(spec=requests.Response)
    mock_response.json.return_value = {test_id: dummy_key}
    patched_requests.get.return_value = mock_response

    # When we get the public key twice
    get_iap_public_key(test_id)
    key = get_iap_public_key(test_id)

    # Then
    assert key == dummy_key

    # The public key is only fetched once
    patched_requests.get.assert_called_once_with('https://www.gstatic.com/iap/verify/public_key')


@patch('census_rm_ops_ui.iap_audit.requests')
def test_get_iap_public_key_cache_refresh(patched_requests):
    # Given
    mock_response = Mock(spec=requests.Response)
    mock_response.json.return_value = {'key_1': 'dummy_1'}
    patched_requests.get.return_value = mock_response

    # We get the first key to cache the result
    get_iap_public_key('key_1')

    # Add another key to the response
    mock_response.json.return_value = {'key_1': 'dummy_1', 'key_2': 'dummy_2'}

    # When we get the second key
    actual_key_2 = get_iap_public_key('key_2')

    # Then the cache is refreshed so the second key can be accessed
    assert actual_key_2 == 'dummy_2'
