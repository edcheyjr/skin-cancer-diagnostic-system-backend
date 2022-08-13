import base64
from tokenize import String
from flask_restx import Namespace, fields
from numpy import require

# create a namespace for the user


class UserDto:
    api = Namespace('user', description='User related operations')
    user = api.model('user', {
        'public_id': fields.String(description='User public id'),
        'username': fields.String(required=True, description='User username'),
        'email': fields.String(required=True, description='User email address'),
        'hash_password': fields.String(required=True, description='User password'),
        'role': fields.String(required=True, description='User role'),
        'date_created': fields.DateTime(description='date created'),
        'date_modified': fields.DateTime(description='date modified')
    })
    user_register = api.model('user_register', {
        'username': fields.String(required=True, description='User username'),
        'email': fields.String(required=True, description='User email address'),
        'password': fields.String(required=True, description='User password'),
        'role': fields.String(required=True, description='User role')
    })


# create a namespace for the authentication
class AuthDto:
    api = Namespace('auth', description='Authentication related operations')
    user_auth = api.model('auth_details', {
        'email': fields.String(required=True, description='The email'),
        'password': fields.String(required=True, description='The user password'),
    })
# create patient namespace


class PatientDto:
    api = Namespace('patient', description='Patient related operations')
    patient = api.model('patient', {
        'id': fields.String(description="id"),
        'public_id': fields.String(description='Patient public id'),
        'name': fields.String(required=True, description='Patient username'),
        'email': fields.String(required=True, description='Patient email'),
        'tel': fields.String(require=True, description='Patient telephone'),
        'age': fields.String(required=True, description='Patient age'),
        'sex': fields.String(required=True, description='Patient sex/gender'),
        'DOB': fields.String(required=True, description="Date of Birth"),
        'region': fields.String(required=True, description="region"),
        'city': fields.String(required=True, description='city'),
        'date_created': fields.DateTime(description='date created'),
        'date_modified': fields.DateTime(description='date modified')
    })
    add_patient = api.model('patient', {
        'name': fields.String(required=True, description='Patient username'),
        'email': fields.String(required=True, description='Patient email'),
        'tel': fields.String(require=True, description='Patient telephone'),
        'DOB': fields.String(required=True, description='Patient birthday'),
        'sex': fields.String(required=True, description='Patient sex/gender'),
        'region': fields.String(required=True, description="region"),
        'city': fields.String(required=True, description='city'),
    })

# create a diagnosis sample


class DiagnosisDto:
    api = Namespace(
        'diagnosis', description='patient test & diagnosis records')
    add_diagnosis_record = api.model('diagnosis', {
        'test_name': fields.String(required=True, description='Test name'),
        'test_description': fields.String(required=True, description='Test discription'),
        'test_result': fields.String(description='Test result'),
        'doc_diagnosis': fields.String(description='doc final diagnosis'),
        'doc_recommendation': fields.String(description='doc recommendation'),
        'patient_id': fields.String(description='patients id')
    }
    )
    diagnosis = api.model('diagnosis', {
        'test_id': fields.String(required=True, description='Test id'),
        'test_name': fields.String(required=True, description='Test name'),
        'status': fields.String(required=True, description='Status'),
        'test_description': fields.String(required=True, description='Test discription'),
        'test_result': fields.String(description='Test result'),
        'doc_diagnosis': fields.String(description='doc final diagnosis'),
        'doc_recommendation': fields.String(description='doc recommendation'),
        'patient_id': fields.String(description='patients id'),
        'date_created': fields.DateTime(description='date created'),
        'date_modified': fields.DateTime(description='date modified')
    })


class TestImageDto:
    api = Namespace(
        'test_images', description='test images used in patient test & diagnosis')
    add_image_record = api.model('test_images', {
        'blobs': fields.List(fields.Raw(required=True, description='base64 images')),
        'localization': fields.String(required=True, description='part of the body taken'),
        'test_id': fields.String(required=True, description='test diagnosis associated with'),
    })
    image_record = api.model('test_images', {
        'id': fields.String(required=True),
        'image_id': fields.String(required=True, description="image unique id"),
        'test_id': fields.String(required=True, description='test_id diagnosis associated with'),
        'image_url': fields.String(required=True, description='Image url'),
        'localization': fields.String(required=True, description='part of the body taken'),
        'classification': fields.String(required=True, description='How the image was classified by the model'),
        'confidence': fields.String(required=True, description='model confidence with it\'s prediction'),
        'scores': fields.String(required=True, description='scsore for each class'),
        'date_modified': fields.DateTime(description='date modified'),
        'date_created': fields.DateTime(description='date created')
    })


class ImageDto:
    api = Namespace('image', description='images')
