from pprint import pprint

from flask import Blueprint, request

from census_rm_ops_ui.controllers import case_controller

postcode_search_bp = Blueprint('postcode_search_bp', __name__, template_folder='templates')


@postcode_search_bp.route('/')
def search_postcode():
    postcode = request.args.get('postcode')
    postcode.strip()

    case_request = case_controller.get_case_by_postcode(postcode)

    return pprint(case_request)
