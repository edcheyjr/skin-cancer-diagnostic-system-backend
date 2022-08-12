from flask_restx import Api
from flask import Blueprint

from .main.controller.user_controller import api as user_ns
from .main.controller.auth_controller import api as auth_ns
from .main.controller.patient_controller import api as patient_ns
from .main.controller.patient_records_controller import api as patient_test_records_ns
from .main.controller.image_details_controller import api as image_detail_ns
from .main.controller.image_controller import api as image_ns

# initialize the blueprint
blueprint = Blueprint('api', __name__)

# create the API as a wrapper around the blueprint
api = Api(blueprint,
          title='Ai Powered Skin Health Diagnosis API Services',
          version='1.0',
          description='Ai Powered Skin Health Diagnosis API services running on Flask using CNN and Tensorflow')

# add the namespaces to the API
api.add_namespace(user_ns, path='/user')
api.add_namespace(auth_ns)
api.add_namespace(patient_ns, path='/patient')
api.add_namespace(patient_test_records_ns, path='/patient/tests')
api.add_namespace(image_detail_ns, path='/images')
api.add_namespace(image_ns, path='/get-image')
