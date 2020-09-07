import json

from flask import Blueprint, current_app, render_template, request, url_for, redirect, flash

from census_rm_ops_ui.controllers import case_controller

case_details_bp = Blueprint('case_details_bp', __name__, template_folder='templates',
                            static_folder='static')


@case_details_bp.route('/')
def case_details_results():
    case_id = request.args.get('case_id')

    case_details = case_controller.get_all_case_details(case_id, current_app.config['CASE_API_URL'])
    case_events = case_details.pop('events')
    sorted_case_events = sorted(case_events, key=lambda case_event: case_event['eventDate'])
    for events in sorted_case_events:
        events['eventPayload'] = json.loads(events['eventPayload'])

    return render_template('view_case_details.html', case_details=case_details, case_events=sorted_case_events)


@case_details_bp.route('/questionnaire-id/')
def get_qid_for_linking():
    qid = request.args.get('qid')
    case_id = request.args.get('case_id')

    uac_qid_link = case_controller.get_qid(qid, current_app.config['CASE_API_URL'])
    if uac_qid_link is None:
        flash('QID does not exist in RM', category='error')
        return redirect(url_for('case_details_bp.case_details_results', case_id=case_id))

    return render_template('view_qid_details.html', uac_qid_link=uac_qid_link, case_id=case_id)


@case_details_bp.route('/questionnaire-id/link/', methods=["POST"])
def link_qid_to_case():
    qid = request.form.get('qid')
    case_id = request.form.get('case_id')

    case_controller.submit_qid_link(qid, case_id, current_app.config['CASE_API_URL'])

    flash('QID link has been submitted', category='linked')
    return redirect(url_for('case_details_bp.case_details_results', case_id=case_id))
