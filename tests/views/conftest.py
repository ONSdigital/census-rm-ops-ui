import pytest

from census_rm_ops_ui.setup import create_app


@pytest.fixture
def app_test_client():
    app = create_app('TestConfig')
    test_client = app.test_client()
    return test_client
