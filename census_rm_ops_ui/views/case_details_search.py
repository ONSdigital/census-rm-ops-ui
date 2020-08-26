from flask import Blueprint, current_app, render_template, request

from census_rm_ops_ui.controllers import case_controller

CASE_DETAILS_FIELDS = ('caseId',
                       'estabType',
                       'uprn',
                       'estabUprn',
                       'collectionExerciseId',
                       'surveyType',
                       'addressType',
                       'caseType',
                       'createdDateTime',
                       'addressLine1',
                       'addressLine2',
                       'addressLine3',
                       'townName',
                       'postcode',
                       'organisationName',
                       'addressLevel',
                       'abpCode',
                       'region',
                       'latitude',
                       'longitude',
                       'oa',
                       'lsoa',
                       'lastUpdated',
                       'msoa',
                       'lad',
                       'caseEvents',
                       'handDelivery',
                       'secureEstablishment',
                       'addressInvalid'
                       )

case_details_search_bp = Blueprint('case_details_search_bp', __name__, template_folder='templates',
                                   static_folder='static')


@case_details_search_bp.route('/case_details/')
def case_details_results():
    case_details = request.args.get('case_details')

    matching_cases = case_controller.get_all_case_details(case_details, current_app.config['CASE_API_URL'])
    matching_cases = add_case_details(matching_cases)

    return render_template('view_case_details.html', cases=matching_cases, case_details=case_details)


def add_case_details(matching_cases):
    for case in matching_cases:
        case['case_details'] = ', '.join(case[key] for key in CASE_DETAILS_FIELDS if case.get(key))
    return matching_cases
