import logging

from flask import Blueprint
from structlog import wrap_logger

logger = wrap_logger(logging.getLogger(__name__))

health_bp = Blueprint('health_bp', __name__, static_folder='static', template_folder='templates')


@health_bp.route('/', methods=['GET'])
def health():
    return 'ok'
