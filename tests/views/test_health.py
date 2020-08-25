def test_health(app_test_client):
    response = app_test_client.get('/health/')

    assert response.status_code == 200
    assert b'ok' in response.data
