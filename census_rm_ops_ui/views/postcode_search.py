from pprint import pprint

from flask import Blueprint, render_template, request

from census_rm_ops_ui.controllers import case_controller

postcode_search_bp = Blueprint('postcode_search_bp', __name__, template_folder='templates', static_folder='static')


@postcode_search_bp.route('/')
def search_postcode():
    postcode = request.args.get('postcode')
    stripped_postcode = postcode.replace(' ', '')

    matching_cases = case_controller.get_case_by_postcode(stripped_postcode)

    for case in matching_cases:
        case['address_summery'] = ', '.join(case[key] for
                                            key in ('organisationName',
                                                    'addressLine1',
                                                    'addressLine2',
                                                    'addressLine3',
                                                    'townName',
                                                    'postcode')
                                            if case.get(key))

    pprint(matching_cases)

    return render_template('postcode_results.html', data=matching_cases, postcode=postcode)
