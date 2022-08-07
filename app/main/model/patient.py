from .. import db
import uuid
import datetime


# create a class for the patient model
class Patient(db.Model):
    """ Patient Model for storing patient related details """
    __tablename__ = "patient"

    id = db.Column(db.Integer, primary_key=True)
    public_id = db.Column(db.String(100), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    tel = db.Column(db.String(10), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    sex = db.Column(db.String(20), nullable=False)
    DOB = db.Column(db.DateTime)
    region = db.Column(db.String(50), nullable=False)
    city = db.Column(db.String(50), nullable=False)
    date_created = db.Column(db.DateTime, default=db.func.current_timestamp())
    date_modified = db.Column(db.DateTime)
    records = db.relationship('Diagnosis', backref='patient', lazy=True)

    def __init__(self, name, age, email, tel, sex, DOB, region, city, date_modified):
        self.public_id = str(uuid.uuid4())
        self.name = name
        self.age = age
        self.email = email
        self.tel = tel
        self.sex = sex
        self.DOB = DOB
        self.region = region
        self.city = city
        self.date_modified = date_modified

    # create a method to serialize the user model
    def serialize(self):
        return {
            'public_id': self.public_id,
            'name': self.name,
            'email': self.email,
            'tel': self.tel,
            'age': self.age,
            'sex': self.sex,
            'DOB': datetime.datetime.strftime(self.DOB, "%d/%m/%Y"),
            'region': self.region,
            'city': self.city,
            'date_created': datetime.datetime.strftime(self.date_created, "%d/%m/%Y, %H:%M:%S"),
            'date_modified': datetime.datetime.strftime(self.date_modified, "%d/%m/%Y, %H:%M:%S")
        }

    # create a method to deserialize the user model
    def deserialize(self, data):
        self.name = data['name']
        self.email = data['email']
        self.tel = data['tel']
        self.age = data['age']
        self.sex = data['sex']
        self.DOB = data['DOB'],
        self.region = data['region'],
        self.city = data['city'],
        self.date_modified = datetime.datetime.now()

    def __repr__(self):
        return '<Patient %r>' % self.name  # return the patient's name
