from pprint import pprint

from flask import Blueprint, request, render_template

from census_rm_ops_ui.controllers import case_controller

postcode_search_bp = Blueprint('postcode_search_bp', __name__, template_folder='templates')


@postcode_search_bp.route('/')
def search_postcode():
    postcode = request.args.get('postcode')
    stripped_postcode = postcode.replace(' ', '')

    case_request = case_controller.get_case_by_postcode(stripped_postcode)

    pprint(case_request)

    return render_template('postcode_results.html', data=case_request, postcode=postcode)
