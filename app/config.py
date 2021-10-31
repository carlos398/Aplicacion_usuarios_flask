from logging import DEBUG


class Config(object):
    SECRET_KEY = 'my_secret_key'
    MAIL_SERVER = 'smtp.gmail.com'
    MAIL_PORT = 465
    MAIL_USE_SSL = True
    MAIL_USE_TLS = False
    MAIL_USERNAME = 'ouremail@gmail.com'
    MAIL_PASSWORD = 'ourpassword'


class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'mysql://root:@localhost/gestion_usrs'
    SQLALCHEMY_TRACK_MODIFICATIONS = False