import uuid
import datetime

from .. import db


class Image(db.Model):
    """ Image Model for storing patient test_sample images and related details"""
    __tablename__ = "test_images"

    id = db.Column(db.Integer, primary_key=True)
    image_id = db.Column(db.String(100), unique=True, nullable=False)
    test_id = db.Column(db.String(100), db.ForeignKey("diagnosis.test_id"))
    image_url = db.Column(db.String(200), nullable=False)
    localization = db.Column(db.String(50), nullable=False)
    classification = db.Column(db.String(100), nullable=True)
    confidence = db.Column(db.Float, nullable=True)
    scores = db.Column(db.String(100), nullable=True)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime)

    def __init__(self, image_url, localization, classification, confidences, scores, test_id, date_modified):
        self.image_id = str(uuid.uuid4())
        self.test_id = test_id
        self.image_url = image_url
        self.localization = localization
        self.classification = classification
        self.confidence = confidences
        self.scores = scores
        self.date_modified = date_modified

    def serialize(self):
        return {
            'image_id': self.image_id,
            'test_id': self.test_id,
            'image_url': self.image_url,
            'localization': self.localization,
            'classification': self.classification,
            'confidence': self.confidence,
            'scores': self.scores,
            'date_created': datetime.datetime.strftime(self.date_created, "%d/%m/%Y, %H:%M:%S"),
            'date_modified': datetime.datetime.strftime(self.date_modified, "%d/%m/%Y, %H:%M:%S")
        }

    def deserialize(self, data):
        self.image_id: data['image_id']
        self.image_url: data['image_url']
        self.localization: data['localization']
        self.classification = data['classification']
        self.confidence = data['confidence']
        self.scores = data['scores']
        self.date_modified: data['date_modified']

    # store model class a string
    def __repr__(self) -> str:
        return "<Image %r>" % self.image_id
