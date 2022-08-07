
from flask import make_response, request
from flask_restx import Resource
from sqlalchemy import null

from ..service import patient_service
from ..utils.dto import PatientDto
from ..utils.decorator import token_required

# create a namespace for the patient controller
api = PatientDto.api
_patient = PatientDto.patient
_add_patient = PatientDto.add_patient


@api.route('')
class PatientList(Resource):
    @token_required
    @api.doc("list of all the patients")
    @api.marshal_list_with(_patient)
    def get(self):
        """List all the patient"""
        return patient_service.get_all_patients()

    @token_required
    @api.response(201, "Patient successfull created")
    @api.doc("create a new patient")
    @api.expect(_add_patient, validate=True)
    def post(self):
        """Create a new patient"""
        data = request.json
        return patient_service.save_new_patient(data)

#  with id arguments


@api.route('/<public_id>')
class PatientList(Resource):
    @token_required
    @api.doc("get a patient with the id")
    @api.marshal_list_with(_patient)
    def get(self, public_id):
        """get a Patient with the id"""
        patient = patient_service.get_a_patient(public_id)
        # store patient id
        # session['patient_id'] = public_id
        if patient.public_id == null:
            make_response({"error", "unauthorized request"}, 401)
        else:
            if not patient:
                api.abort(404, "User not found")
            return patient

    @token_required
    @api.doc("update a patient with the id")
    def put(self, public_id):
        """ update Patient with the id"""
        patient = patient_service.get_a_patient(public_id)
        data = request.json
        if patient.public_id == null:
            make_response({"error", "unauthorized request"}, 401)
        else:
            if not patient:
                api.abort(404, "User not found")
            return patient_service.update_a_patient(public_id, data)

    @token_required
    @api.doc("delete a patient with the id")
    # @api.marshal_list_with(_patient)
    def delete(self, public_id):
        """delete Patient"""
        patient = patient_service.get_a_patient(public_id)
        if patient.public_id == null:
            make_response({"error", "unauthorized request"}, 401)
        else:
            if not patient:
                api.abort(404, "User not found")
            return patient_service.delete_a_patient(public_id)
