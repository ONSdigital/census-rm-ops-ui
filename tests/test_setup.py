import os

from flask import app

from census_rm_ops_ui.setup import create_app
from config import TestConfig


def test_create_app():
    # Given
    app.testing = True
    os.environ['APP_SETTINGS'] = 'TestConfig'

    # When
    test_app = create_app()

    # Then
    # Check the app has been initialized with the given test config
    assert test_app.config['CASE_API_URL'] == TestConfig.CASE_API_URL
