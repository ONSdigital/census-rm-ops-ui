from flask import Blueprint, current_app, render_template, request

from census_rm_ops_ui.controllers import case_controller

case_details_bp = Blueprint('case_details_bp', __name__, template_folder='templates',
                                   static_folder='static')


@case_details_bp.route('/')
def case_details_results():
    case_id = request.args.get('case_id')

    case_details = case_controller.get_all_case_details(case_id, current_app.config['CASE_API_URL'])
    case_events = case_details['events']
    sorted_case_events = sorted(case_events, key=lambda case_event:case_event['eventDate'])
    case_details.pop('events')

    return render_template('view_case_details.html', case_details=case_details, case_events=sorted_case_events)


# def add_case_details(matching_cases):
#     for case in matching_cases:
#         case['case_details'] = ', '.join(case[key] for key in CASE_DETAILS_FIELDS if case.get(key))
#     return matching_cases
