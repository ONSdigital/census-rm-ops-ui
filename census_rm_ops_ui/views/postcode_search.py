from flask import Blueprint, current_app, render_template, request

from census_rm_ops_ui.controllers import case_controller

ADDRESS_SUMMARY_FIELDS = ('organisationName',
                          'addressLine1',
                          'addressLine2',
                          'addressLine3',
                          'townName',
                          'postcode')

postcode_search_bp = Blueprint('postcode_search_bp', __name__, template_folder='templates', static_folder='static')


@postcode_search_bp.route('/')
def postcode_search():
    return render_template('postcode_search.html')


@postcode_search_bp.route('/postcode/')
def postcode_results():
    postcode = request.args.get('postcode')

    matching_cases = case_controller.get_cases_by_postcode(postcode, current_app.config['CASE_API_URL'])
    matching_cases = add_address_summaries(matching_cases)

    return render_template('postcode_results.html', cases=matching_cases, postcode=postcode)


def add_address_summaries(matching_cases):
    for case in matching_cases:
        case['address_summary'] = ', '.join(case[key] for key in ADDRESS_SUMMARY_FIELDS if case.get(key))
    return matching_cases
