import datetime

from sqlalchemy import null
from .. import db
from ..model.patient_records import Diagnosis
from ..service.patient_service import get_a_patient
from ..config import SUCCESS, FAILURE
from ..utils.save_to_db import save_changes


# data keys
test_keys = ['test_name', 'test_description',
             'test_result', 'doc_diagnosis', 'doc_recommendation']
# create intial test and dignosis data


def save_intial_test(patient_id, data):
    try:
        patient = get_a_patient(patient_id)

        if patient:
            patient_test = Diagnosis.query.filter_by(
                patient_id=patient_id, status="active").first()
            if not patient_test:
                new_diagnosis = Diagnosis(
                    test_name=data['test_name'],
                    test_description=data['test_description'],
                    test_result=data['test_result'],
                    doc_diagnosis=data['doc_diagnosis'],
                    doc_recommendation=data['doc_recommendation'],
                    patient_id=patient_id,
                    date_modified=datetime.datetime.now(),
                    status='active'
                )
                save_changes(new_diagnosis)
            else:
                response = {
                    'status': FAILURE,
                    'message': 'their is a test still underway...'
                }
                return response, 409
            return {
                "status": SUCCESS,
                "message": "created a new diagnosis record"
            }, 201
    except Exception as e:
        return {
            'status': FAILURE,
            'message': f'server error{e}'
        }, 500

# get the tests and diagnosis data


def get_all_test(patient_id):
    try:
        diagnosis = Diagnosis.query.filter_by(patient_id=patient_id).all()
        # print("-------------------------------------")
        # print("patient", diagnosis.patient)
        # print("-------------------------------------")
        return diagnosis

    except Exception as e:
        return {
            'status': FAILURE,
            'message': f'server error{e}'
        }, 500

# get one test


def get_a_test(test_id):
    try:
        patient_test_record = Diagnosis.query.filter_by(
            test_id=test_id).first()
        if patient_test_record:
            return patient_test_record, 200
        return{
            'status': FAILURE,
            'message': 'tests not found'
        }, 404
    except Exception as e:
        return {
            'status': FAILURE,
            'message': f'server error{e}'
        }, 500

# update patient test records


def update_a_test(test_id, data):
    try:
        patient_test_record = Diagnosis.query.filter_by(
            test_id=test_id).first()
        if patient_test_record:
            if test_keys[0] in data.keys():
                patient_test_record.test_name = data['test_name']
            if test_keys[2] in data.keys():
                patient_test_record.test_result = data['test_result']
            if test_keys[1] in data.keys():
                patient_test_record.test_description = data['test_description']
            if test_keys[3] in data.keys():
                patient_test_record.doc_diagnosis = data['doc_diagnosis']
                # change to inactive
                patient_test_record.status = "inactive"
            if test_keys[4] in data.keys():
                patient_test_record.doc_recommendation = data['doc_recommendation']
            patient_test_record.date_modified = datetime.datetime.now()
            # commit the session
            db.session.commit()
            return {
                'status': SUCCESS,
                'message': 'successfully updated the patient records'
            }, 200
        return {
            'status': FAILURE,
            'message': 'records not found'
        }, 404
    except Exception as e:
        return {
            'status': FAILURE,
            'message': f'server error{e}'
        }, 500

# delete patient test record


def delete_a_test(test_id):
    try:
        patient_test_record = Diagnosis.query.filter_by(
            test_id=test_id).first()
        if patient_test_record:
            Diagnosis.query.filter_by(test_id=test_id).delete()
            db.session.commit()
            return {
                'status': SUCCESS,
                'message': 'successfully deleted the patient record'
            }, 200
        return {
            'status': FAILURE,
            'message': 'records not found'
        }, 404
    except Exception as e:
        return {
            'status': FAILURE,
            'message': f'server error{e}'
        }, 500

# delete all patients records


def delete_all_test(patient_id):
    # patient = get_a_patient(patient_id)
    try:
        Diagnosis.query.filter_by(patient_id=patient_id).delete()
        db.session.commit()
        return {
            'status': SUCCESS,
            'message': 'successfully deleted all the patient records'
        }, 200
    except Exception as e:
        return {
            'status': FAILURE,
            'message': f'server error{e}'
        }, 500

        # save results
