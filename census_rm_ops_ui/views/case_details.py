import json

from flask import Blueprint, current_app, flash, redirect, render_template, request, url_for

from census_rm_ops_ui.controllers import case_controller

case_details_bp = Blueprint('case_details_bp', __name__, template_folder='templates',
                            static_folder='static')


@case_details_bp.route('/')
def case_details_results():
    case_id = request.args['case_id']

    case_details = case_controller.get_all_case_details(case_id, current_app.config['CASE_API_URL'])
    case_events = case_details.pop('events')
    sorted_case_events = sorted(case_events, key=lambda case_event: case_event['rmEventProcessed'])
    for events in sorted_case_events:
        events['eventPayload'] = json.loads(events['eventPayload'])

    return render_template('view_case_details.html', case_details=case_details, case_events=sorted_case_events)


def is_ccs_type_qid(qid):
    qid_type = qid[:2]
    return qid_type in {'51', '52', '53', '54', '61', '62', '63', '71', '73', '81', '83', }


@case_details_bp.route('/link-qid/')
def get_qid_for_linking():
    qid = request.args['qid']
    case_id = request.args['case_id']

    uac_qid_link = case_controller.get_qid(qid, current_app.config['CASE_API_URL'])
    if uac_qid_link is None:
        flash('QID does not exist in RM', category='error')
        return redirect(url_for('case_details_bp.case_details_results', case_id=case_id))

    case = case_controller.get_summary_case_details(case_id, current_app.config['CASE_API_URL'])
    if is_ccs_type_qid(qid) and not case['surveyType'] == 'CCS':
        flash('Linking a CCS QID to a non CCS case is forbidden', category='error')
        return redirect(url_for('case_details_bp.case_details_results', case_id=case_id))
    if not is_ccs_type_qid(qid) and case['surveyType'] == 'CCS':
        flash('Linking a non CCS QID to a CCS case is forbidden', category='error')
        return redirect(url_for('case_details_bp.case_details_results', case_id=case_id))

    return render_template('link_qid_to_case.html', uac_qid_link=uac_qid_link, case_id_to_link=case_id)


@case_details_bp.route('/link-qid/submit/', methods=["POST"])
def link_qid_to_case():
    qid = request.form['qid']
    case_id = request.form['case_id']

    case_controller.submit_qid_link(qid, case_id, current_app.config['CASE_API_URL'])

    flash('QID link has been submitted', category='linked')
    return redirect(url_for('case_details_bp.case_details_results', case_id=case_id))
