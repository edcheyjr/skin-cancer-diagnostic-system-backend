from flask_restx import Resource
from flask import send_file
from ..utils.dto import ImageDto
from ..utils.decorator import token_required

# create a  namespace
api = ImageDto.api


@api.route('/<filename>')
class Image(Resource):
    # @token_required
    @api.doc('return images for display from storage')
    def get(self, filename):
        """return images for display from storage"""
        fileArr = filename.split('.')
        filepath = f'storage/{filename}'
        return send_file(filepath, mimetype=f'image/{fileArr[1]}')

# one way send_file() from flask
# another way is to get the image from storage send it as  base64 store in localstorage will converting it to image and displaying it.
