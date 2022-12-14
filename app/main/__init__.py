from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager
from flask_cors import CORS
from flask_session import Session
from .config import config_by_name, db


# db = SQLAlchemy()
flask_bcrypt = Bcrypt()
migrate = Migrate()
jwt = JWTManager()
cors = CORS()
sess = Session()


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config_by_name[config_name])
    db.init_app(app)
    # sess.init_app(app)
    cors.init_app(app)
    flask_bcrypt.init_app(app)
    # jwt.init_app(app)
    migrate.init_app(app, db)

    return app
