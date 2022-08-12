import datetime
from app.main.model.patient_records import Diagnosis
from app.main.model.test_images import Image
from .. import db
from ..model.patient import Patient
from ..model.patient_records import Diagnosis
from ..config import FAILURE, SUCCESS
from ..utils.save_to_db import save_changes

# create a method to create and save a new patient
allowed_gender = ['male', 'female']


def save_new_patient(data):
    try:
        birthdate_obj = datetime.datetime.strptime(
            # gmt :%SZ
            # day abbr %a
            data['DOB'], "%b/%d/%Y %H:%M:%S")
        age = datetime.datetime.now().year - birthdate_obj.year
        patient = Patient.query.filter_by(email=data["email"]).first()
        print("==================================")
        print("---------", patient, "------------")
        print("==================================")
        if patient:
            return {
                "status": FAILURE,
                "message": "patient records already exist"
            },  409
        if len(data['tel']) != 10:
            return {
                "status": FAILURE,
                "message": "tel number can only be 10 digit"
            }, 400

        if not isinstance(age, int):
            return {
                "status": FAILURE,
                "message": "age is an integer not string"
            }, 400
        if data['sex'].lower() not in allowed_gender:
            return {
                "status": FAILURE,
                "message": "gender can be male or female only"
            }, 400

        new_patient = Patient(
            name=data["name"],
            email=data['email'],
            tel=data['tel'],
            age=age,
            sex=data['sex'],
            DOB=birthdate_obj,
            region=data['region'],
            city=data['city'],
            date_modified=datetime.datetime.now()
        )

        save_changes(new_patient)
        return {
            "status": SUCCESS,
            "message": "add a new patient"
        }, 201
    except Exception as e:
        return{
            "status": FAILURE,
            "message": f"failed to add a patient {e}"
        }, 500

# create a methods to get all patients


def get_all_patients():
    try:
        patient = Patient.query.all()
        #
        # print("=============================")
        # print("records", patient.records)
        # print("=============================")
        return patient
    except Exception as e:
        return{
            "status": FAILURE,
            "message": f"failed to get a patient {e}"
        }, 500
# create a method to get a patient by id


def get_a_patient(id):
    return Patient.query.filter_by(public_id=id).first_or_404()

# delete a patient


# update patient method


def update_a_patient(id, data):
    keys = ["name", "email", "tel", "DOB", "sex", "city", "region"]

    if data:
        data_obj = dict(data)
    try:
        patient = Patient.query.filter_by(public_id=id).first()

        print("============================")
        print("patient", patient)
        print("============================")
        if patient:
            if keys[0] in data.keys() and data_obj["name"] != "":
                patient.name = data_obj["name"]
            if keys[1] in data.keys() and data_obj["email"] != "":
                patient.email = data_obj["email"]
            if keys[2] in data.keys() and data_obj["tel"] != "":
                patient.tel = data_obj["tel"]
            if keys[3] in data.keys() and data_obj["DOB"] != "":
                birthdate_obj = datetime.datetime.strptime(
                    # gmt :%SZ
                    # day abbr %a
                    data['DOB'], "%b/%d/%Y %H:%M:%S")
                patient.DOB = birthdate_obj
                patient.age = datetime.datetime.now().year - birthdate_obj.year
            if keys[4] in data.keys() and data_obj["sex"] != "":
                patient.sex = data_obj['sex']
            if keys[5] in data.keys() and data_obj["city"] != "":
                patient.city = data_obj['city']
            if keys[6] in data.keys() and data_obj["region"] != "":
                patient.region = data_obj['region']

            patient.date_modified = datetime.datetime.now()
            # instance.update(
            #     data
            # )
            db.session.commit()
            return {
                "status": SUCCESS,
                "message": "patient info updated",
                "data": Patient.serialize(patient)
            }, 200
        else:
            return {
                "status": FAILURE,
                "message": "patient not found"
            }, 404
    except Exception as e:
        print("error", e)
        return {
            "status": FAILURE,
            "message": "failed to update patient"
        }, 500


def delete_a_patient(id):
    patient = Patient.query.filter_by(public_id=id).first()
    try:
        if patient:

            Patient.query.filter_by(public_id=id).delete()
            Diagnosis.query.filter_by(patient_id=id).delete()
            db.session.commit()
            return {
                "status": SUCCESS,
                "message": " successfully deleted the patient from the system"
            }, 200
        else:
            return {
                'status': FAILURE,
                'message': 'records not found'
            }, 404
    except Exception as e:
        print("error", e)
        return {
            "status": FAILURE,
            "message": f"failed to delete patient{e}"
        }, 500
