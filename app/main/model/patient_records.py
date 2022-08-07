from traitlets import default
from .. import db
import uuid
import datetime


# create a class for the patient model
class Diagnosis(db.Model):
    """ Diagnosis Model for storing patient tests and diagnosis related details """
    __tablename__ = "diagnosis"

    id = db.Column(db.Integer, primary_key=True)
    test_id = db.Column(db.String(100), unique=True, nullable=False)
    patient_id = db.Column(db.String(100), db.ForeignKey("patient.public_id"))
    status = db.Column(db.String(10), nullable=False, default="active")
    test_name = db.Column(db.String(100), nullable=False)
    test_description = db.Column(db.String(100), nullable=False)
    test_result = db.Column(db.String(100), nullable=True)
    doc_diagnosis = db.Column(db.String(200), nullable=True)
    doc_recommendation = db.Column(db.String(500), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime)
    images = db.relationship('Image', backref="diagnosis", lazy=True)

    def __init__(self, test_name, test_description, test_result, doc_diagnosis, doc_recommendation, patient_id, status, date_modified):
        self.test_id = str(uuid.uuid4())
        self.test_name = test_name
        self.test_description = test_description
        self.test_result = test_result
        self.doc_diagnosis = doc_diagnosis
        self.doc_recommendation = doc_recommendation
        self.date_modified = date_modified
        self.patient_id = patient_id
        self.status = status

    def serialize(self):
        return {
            'test_id': self.test_id,
            'test_name': self.test_name,
            'test_description': self.test_description,
            'test_result': self.test_result,
            'doc_diagnosis': self.doc_diagnosis,
            'status': self.status,
            'doc_recommendation': self.doc_recommendation,
            'date_created': datetime.datetime.strftime(self.date_created, "%d/%m/%Y, %H:%M:%S"),
            'date_modified': datetime.datetime.strftime(self.date_modified, "%d/%m/%Y, %H:%M:%S")
        }

    def deserialize(self, data):
        self.test_name = data['test_name']
        self.test_description = data['test_description']
        self.test_result = data['test_result']
        self.doc_diagnosis = data['doc_diagnosis']
        self.status = data["status"]
        self.doc_recommendation = data['doc_recommendation']
        self.date_modified = data['date_modified']

    def __repr__(self) -> str:
        return '<Diagnosis %r>' % self.id  # return the test id number
