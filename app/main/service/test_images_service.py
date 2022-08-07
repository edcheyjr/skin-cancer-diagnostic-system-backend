import datetime

from sqlalchemy import null
from .. import db
from ..model.test_images import Image
from ..service.patient_records_service import get_a_test
from ..config import SUCCESS, FAILURE
from ..utils.save_to_db import save_changes


# save test image records
def save_image_records(test_id, data):
    try:
        test_record = get_a_test(test_id)
        if test_record:
            new_image_record = Image(
                data['image_url'],
                data['localization'],
                data['classification'],
                data['confidence'],
                test_id,
                datetime.datetime.now()
            )
            save_changes(new_image_record)
            return {
                'status': SUCCESS,
                'message': 'image was classified successfully'
            }, 201
        return{
            'status': FAILURE,
            'message': 'image details not found'
        }, 404
    except Exception as e:
        return{
            'status': FAILURE,
            'message': f'Error message {e}'
        }, 500

# get all images detail related to a test and diagnosis records of a patient


def get_all_images_details(test_id):
    try:
        return Image.query.filter_by(test_id=test_id).all()
    except Exception as e:
        return {
            'status': FAILURE,
            'message': f'Error message {e}'
        }, 500

# get a image detail related to a test and diagnosis records of a patient


def get_a_image_details(image_id):
    try:
        return Image.query.filter_by(image_id=image_id).first_or_404()
    except Exception as e:
        return{
            'status': FAILURE,
            'message': f'Error message {e}'
        }, 500

# delete image detail related to a test and diagnosis records of a patient


def delete_a_image_detail(image_id):
    try:
        image_detail = Image.query.filter_by(image_id=image_id).first()
        if image_detail:
            Image.query.filter_by(image_id=image_id).delete()
            db.session.commit()
            return {
                'status': SUCCESS,
                'message': 'successfully deleted image details'
            }, 200
        return{
            'status': FAILURE,
            'message': 'image details not found'
        }, 404
    except Exception as e:
        return{
            'status': FAILURE,
            'message': f'Error message {e}'
        }, 500


# delete all images related to a test record
def delete_all_image_details_related_to_test(test_id):
    try:
        Image.query.filter_id(test_id=test_id).delete()
        db.session.commit()
        return{
            'status': SUCCESS,
            'message': 'successfully deleted the patient test image details'
        }, 200
    except Exception as e:
        return {
            'status': FAILURE,
            'message': f'Error message {e}'
        }, 500
