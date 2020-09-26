import os
basedir=os.path.abspath(os.path.dirname(__file__))

class Config:       # base class
    SECRET_KEY=os.environ.get('SECRET_KEY') or 'hard to guess string'
    SQLALCHEMY_TRACK_MODIFICATIONS=False
    
    MAIL_SERVER=os.environ.get('MAIL_SERVER','smtp.gmail.com')
    MAIL_PORT=int(os.environ.get('MAIL_PORT','587'))
    MAIL_USE_TLS=os.environ.get('MAIL_USE_TLS','true').lower() in ['true','on','1']
    MAIL_USERNAME=os.environ.get('MAIL_USERNAME')
    MAIL_PASSWORD=os.environ.get('MAIL_PASSWORD')
    CIRR_MAIL_SUBJECT_PREFIX='Reset your password'
    CIRR_MAIL_SENDER='it@nedfi.com'
    CIRR_ADMIN=os.environ.get('CIRR_ADMIN') or 'it@nedfi.com'
    CONSUMER_REQ_PER_PAGE=os.environ.get('CONSUMER_REQ_PER_PAGE') or 15
    ALLOWED_FILE_EXTENSIONS=['jpg','png','pdf','txt']
    UPLOAD_FOLDER=os.path.realpath('.')+'/app/static/uploads/'
    MAX_CONTENT_LENGTH=50*1024*1024

    @staticmethod
    def init_app(app):
        pass

class DevelopmentConfig(Config):     #sub class
    DEBUG=True
    SQLALCHEMY_DATABASE_URI= os.environ.get('DEV_DATABASE_URL') or 'mysql+pymysql://root:@localhost/cirrdev'

class TestingConfig(Config):       #sub class
    TESTING=True
    SQLALCHEMY_DATABASE_URI=os.environ.get('TEST_DATABASE_URL') or 'mysql+pymysql://root:@localhost/cirrtest'
class ProductionConfig(Config):       #sub class
    SQLALCHEMY_DATABASE_URI=os.environ.get('DATABASE_URL') or 'mysql+pymysql://root:@localhost/cirr'

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig

}
