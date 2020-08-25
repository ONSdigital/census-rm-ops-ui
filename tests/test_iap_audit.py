import json

import responses

from census_rm_ops_ui.iap_audit import get_iap_public_key
from tests import unittest_helper


@responses.activate
def test_get_iap_public_key():
    # Given
    test_id = 'test_id'
    dummy_key = 'dummy_key'
    responses.add(responses.GET, 'https://www.gstatic.com/iap/verify/public_key',
                  body=json.dumps({test_id: dummy_key}))

    # When we get the public key twice
    get_iap_public_key(test_id)
    key = get_iap_public_key(test_id)

    # Then
    unittest_helper.assertEqual(key, dummy_key)


@responses.activate
def test_get_iap_public_key_cache_refresh():
    # Given
    responses.add(responses.GET, 'https://www.gstatic.com/iap/verify/public_key',
                  body=json.dumps({'key_1': 'dummy_1'}))

    # We get the first key to cache the result
    get_iap_public_key('key_1')

    # Add another key to the response
    responses.remove(responses.GET, 'https://www.gstatic.com/iap/verify/public_key')
    responses.add(responses.GET, 'https://www.gstatic.com/iap/verify/public_key',
                  body=json.dumps({'key_1': 'dummy_1', 'key_2': 'dummy_2'}))

    # When we get the second key
    actual_key_2 = get_iap_public_key('key_2')

    # Then the cache is refreshed so the second key can be accessed
    unittest_helper.assertEqual(actual_key_2, 'dummy_2')
