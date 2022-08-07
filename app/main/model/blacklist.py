from .. import db

class Blacklisted (db.Model):
    __tablename__ = 'blacklisted'

    id = db.Column(db.Integer, primary_key=True)
    token = db.Column(db.String(500), unique=True, nullable=False)
    blacklisted_on = db.Column(db.DateTime, default=db.func.current_timestamp())

    def __init__(self, token):
        self.token = token

    def serialize(self):
        return { 
            'id': self.id,
            'token': self.token,
            'blacklisted_on': self.blacklisted_on  
        } 

    def deserialize(self, data): 
        self.id = data['id']  
        self.token = data['token']
        self.blacklisted_on = data['blacklisted_on']
    
    def __repr__(self):
        return '<id: token: {}'.format(self.token)

    @staticmethod
    def is_token_blacklisted(decoded_token):
        # check if the token is blacklisted
        result = Blacklisted.query.filter_by(token=decoded_token).first()
        return bool(result)
