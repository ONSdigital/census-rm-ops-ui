import json
import logging
import os

from structlog import wrap_logger

from census_rm_ops_ui.logger import logger_initial_config


def test_json_logging(caplog):
    # Given
    os.environ['JSON_INDENT_LOGGING'] = '1'
    logger_initial_config()
    logger = wrap_logger(logging.getLogger())

    # When
    logger.error('Test')
    message_json = json.loads(caplog.records[-1].getMessage())

    # Then
    message_contents = {"event": "Test", "level": "error", "service": "census-rm-ops-ui"}
    for key, value in message_contents.items():
        assert message_json[key] == value
