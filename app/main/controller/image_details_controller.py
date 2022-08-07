from dataclasses import Field
from flask import make_response, request, jsonify
from flask_restx import Resource, reqparse
from sqlalchemy import null
from werkzeug.utils import secure_filename
from werkzeug.datastructures import FileStorage
from os import path, mkdir
import datetime
import time

from app.main.config import FAILURE, SUCCESS, UPLOAD_FOLDER
from app.main.utils.base64_decode import base64ToPngOrJpgConverter
from app.main.utils.check_file import is_file_allowed
from app.main.utils.label_mapper import label_mapper

from ..service import test_images_service
from ..utils.dto import TestImageDto
from ..utils.decorator import token_required
from ...model.model import Model


# create namespace
api = TestImageDto.api
_add_image_detail = TestImageDto.add_image_record
_image_details = TestImageDto.image_record


@api.route('', methods=['POST', 'GET'])
class ImageList(Resource):
    def __init__(self, api=None, *args, **kwargs):
        super().__init__(api, *args, **kwargs)
        self.parser = reqparse.RequestParser()

    @token_required
    @api.doc("list of all the patients")
    @api.marshal_list_with(_image_details, envelope='data')
    def get(self):
        """get all image details related to a test and diagnosis record"""
        data = request.json
        return test_images_service.get_all_images_details(data['test_id'])

    @token_required
    @api.doc("add a new image")
    @api.expect(_add_image_detail)
    def post(self):
        """add a new image and make classifiction"""
        # Part 1: add arguments in the post request
        # self.parser.add_argument(
        #     "file", type=FileStorage, location='files', required=True, action="append")
        # self.parser.add_argument('localization')
        # self.parser.add_argument('test_id')
        # self.parser.add_argument(
        #     "data", location='json', required=True, action="append")

        # Part 2: parse the request
        # args = self.parser.parse_args()
        # if 'file' not in args:
        #     resp = jsonify({
        #         'status': FAILURE,
        #         'message': 'No file part in the request'
        #     })
        #     resp.status_code = 400
        #     return resp
        # imagefileArr = args['file']  # get all the files
        data = request.json
        if not bool(data['blobs']):
            return{
                "status": FAILURE,
                "message": "no image file selected"
            }, 400
        for blob in data['blobs']:
            # check if the post request has the file part
            # if imagefile.filename == '':
            #     resp = jsonify({'status': FAILURE,
            #                     'message': 'No file selected'
            #                     })
            #     resp.status_code = 400
            # if imagefile and is_file_allowed(imagefile.filename):
            #     filename = secure_filename(imagefile.filename)
            #     # check if the dir exists
            #     if not path.exists(UPLOAD_FOLDER):
            #         mkdir(UPLOAD_FOLDER)
            #     filepath = path.join(UPLOAD_FOLDER, filename)
            #     imagefile.save(filepath)
            date = datetime.datetime.now()
            image_id = time.mktime(date.timetuple())
            print("==================")
            print('date', image_id)
            print("==================")
            try:
                filepath, filename = base64ToPngOrJpgConverter(
                    blob, int(image_id), data['test_id'])
            except Exception as e:
                return{
                    'status': FAILURE,
                    'message': f'err while decoding : {e}'
                }, 500
            try:
                if bool(filepath):
                    if is_file_allowed(filename):
                        # push the file to the model for prediction
                        new_model = Model(None)
                        model = new_model.load_pre_trained_model()
                        print('---------------')
                        print('loading model...', model)
                        print('---------------')
                        label, conf = new_model.predict_single_image(
                            model=model, file_name=filename, img_path=filepath)
                        res_data = {
                            'image_url': filepath,
                            'localization': data['localization'],
                            'classfication': label_mapper(label),
                            'confidence': conf
                        }
                        test_images_service.save_image_records(
                            data['test_id'], res_data)
                        return {
                            'status': SUCCESS,
                            'test_id': data['test_id'],
                            'file': filepath,
                            'localization': data['localization'],
                            'result': {
                                'label': label,
                                'conf': conf
                            }
                        }, 200
                    else:
                        resp = jsonify(
                            {'status': FAILURE, 'message': 'Allowed file types are png, jpg, jpeg, gif'})
                        resp.status_code = 400
                        return resp
            except Exception as e:
                return{
                    'status': FAILURE,
                    'message': f'err while predicting : {e}'
                }, 500
