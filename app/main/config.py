import os

# uncomment the line below for postgres database url from environment variable
# postgres_local_base = os.environ['DATABASE_URL']

basedir = os.path.abspath(os.path.dirname(__file__))


class Config:
    SECRET_KEY = os.getenv('SECRET_KEY')
    DEBUG = False
    SUCCESS = "success"
    FAILURE = "fail"
    # Flask-Session
    SESSION_TYPE = os.getenv('SESSION_TYPE')
    UPLOAD_IMG_EXTENSION = ['jpg', 'jpeg', 'png', 'gif']
    MAX_CONTENT_LENGTH = os.getenv(
        'MAX_CONTENT_LENGTH') or 50 * 1024 * 1024  # max file size
    UPLOAD_FOLDER = os.path.join(basedir, 'storage')  # uploads folder
    # if SESSION_TYPE == 'redis')
    # SESSION_REDIS = redis.from_url(os.getenv('SESSION_REDIS'))
    # redis.Redis()


class DevelopmentConfig(Config):
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'flask_main.db'))
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS', False)


class TestingConfig(Config):
    DEBUG = True
    TESTING = True
    SQLALCHEMY_DATABASE_URI = os.getenv(
        'DATABASE_URL', 'sqlite:///' + os.path.join(basedir, 'flask_main.db'))
    PRESERVE_CONTEXT_ON_EXCEPTION = os.getenv(
        'PRESERVE_CONTEXT_ON_EXCEPTION', False)
    SQLALCHEMY_TRACK_MODIFICATIONS = os.getenv(
        'SQLALCHEMY_TRACK_MODIFICATIONS', False)


class ProductionConfig(Config):
    DEBUG = False
    # uncomment the line below to use postgres
    # SQLALCHEMY_DATABASE_URI = postgres_local_base


config_by_name = dict(
    development=DevelopmentConfig,
    test=TestingConfig,
    production=ProductionConfig
)

key = Config.SECRET_KEY
SUCCESS = Config.SUCCESS
FAILURE = Config.FAILURE
UPLOAD_FOLDER = Config.UPLOAD_FOLDER
ALLOWED_EXTENSION = Config.UPLOAD_IMG_EXTENSION