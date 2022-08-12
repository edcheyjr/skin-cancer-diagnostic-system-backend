from flask import request, session
from flask_restx import Resource
from sqlalchemy import null
import pickle

from app.main.utils.decorator import token_required

from ..service import patient_records_service
from ..utils.dto import DiagnosisDto
from ..utils.manage_session_data import get_session_data
from ..config import FAILURE, SUCCESS
# filename
filename = "patient_data.txt"

# create a namespace
api = DiagnosisDto.api
_patient_record = DiagnosisDto.diagnosis
_add_patient_record = DiagnosisDto.add_diagnosis_record


@api.route('')
class PatientRecord(Resource):

    @token_required
    @api.doc("all test and diagnosis records of the patient")
    @api.marshal_with(_patient_record, as_list=True)
    def get(self):
        """all test and diagnosis records of the patient"""
        session_data_list = get_session_data(filename)
        patient_id = session_data_list[0]

        print("========================")
        print("session data", patient_id)
        print("========================")
        records = patient_records_service.get_all_test(
            patient_id=patient_id)
        if bool(records):
            return records
        return {
            "status": FAILURE,
            "message": "no test records of the patient"
        }, 404

    @token_required
    @api.doc("post a new test record for the patient")
    @api.expect(_add_patient_record, validate=True)
    def post(self):
        """post a new test record for the patient"""
        session_data_list = get_session_data(filename)
        patient_id = session_data_list[0]
        data = request.json
        return patient_records_service.save_intial_test(patient_id, data)

    @token_required
    @api.doc("post a new test record for the patient")
    def delete(self):
        data = request.json
        return patient_records_service.delete_all_test(data['patient_id'])


@api.route('/<test_id>')
class PatientRecord(Resource):
    @token_required
    @api.doc("get a specific test record")
    @api.marshal_with(_patient_record)
    def get(self, test_id):
        """get a test"""
        data = request.json
        return patient_records_service.get_a_test(test_id=test_id, status=data['status'])

    @token_required
    @api.doc("update a specific test record")
    def put(self, test_id):
        """update a specific test and diagnosis record"""
        data = request.json
        return patient_records_service.update_a_test(test_id=test_id, data=data)

    @token_required
    @api.doc("delete a specific test record")
    def delete(self, test_id):
        """delete a specific test record"""
        return patient_records_service.delete_a_test(test_id=test_id)
