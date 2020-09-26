from werkzeug.security import generate_password_hash,check_password_hash
from flask_login import UserMixin, AnonymousUserMixin
from . import login_manager,db
from flask import current_app
from datetime import datetime
datetime.utcnow()
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer

class Permission:
    WRITE=1
    ADMIN=2

class Role(db.Model):
    __tablename__= 'roles'      # name of the table in database
    id = db.Column(db.Integer,primary_key=True, index=True)
    name=db.Column(db.String(64),unique=True, index=True)
    default=db.Column(db.Boolean, default=False, index=True)
    permissions=db.Column(db.Integer)
    users=db.relationship('User',cascade="all,delete-orphan",backref='role',lazy='dynamic')

    def __repr__(self):
        return '<Role %r>' % self.name

    def __init__(self,**kwargs):
        super(Role, self).__init__(**kwargs)
        if self.permissions is None:
            self.permissions=0

    def add_permission(self,perm):
        if not self.has_permission(perm):
            self.permissions += perm
    
    def remove_permission(self,perm):
        if self.has_permission(perm):
            self.permissions -= perm
    
    def reset_permissions(self):
        self.permissions = 0

    def has_permission(self,perm):
        return self.permissions & perm == perm

    @staticmethod
    def insert_roles():
        roles={
            'User':[Permission.WRITE],
            'Report-admin':[Permission.WRITE],
            'Admin':[Permission.WRITE, Permission.ADMIN]
        }
        default_role='User'
        for r in roles:
            role=Role.query.filter_by(name=r).first()
            if role is None:
                role=Role(name=r)
            role.reset_permissions()
            for perm in roles[r]:
                role.add_permission(perm)
            role.default=(role.name==default_role)
            db.session.add(role)
        db.session.commit()
    
    
class User(UserMixin, db.Model):
    __tablename__='users'
    id=db.Column(db.Integer,primary_key=True, index=True)
    name=db.Column(db.String(50))
    email=db.Column(db.String(50), unique=True, index=True)
    username=db.Column(db.String(50), unique=True, index=True)
    location=db.Column(db.String(64))
    about_me=db.Column(db.Text())
    role_id=db.Column(db.Integer,db.ForeignKey('roles.id'))
    consumer_requests=db.relationship('Consumer_request',cascade="all,delete-orphan",backref='user',lazy='dynamic')
    commercial_requests=db.relationship('Commercial_request',cascade="all,delete-orphan",backref='user',lazy='dynamic')
    consumer_reports=db.relationship('Consumer_report',cascade="all,delete-orphan",backref='user',lazy='dynamic')
    commercial_reports=db.relationship('Commercial_report',cascade="all,delete-orphan",backref='user',lazy='dynamic')
    password_hash=db.Column(db.String(128))
    
    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self,password):
        self.password_hash=generate_password_hash(password)  # make plain text to hash

    def verify_password(self,password):
        return check_password_hash(self.password_hash,password)  # to confirm password

    def __init__(self,**kwargs):
        super(User,self).__init__(**kwargs)
        if self.role is None:
            if self.email==current_app.config['CIRR_ADMIN']:
                self.role=Role.query.filter_by(name='Admin').first()
            if self.role is None:
                self.role = Role.query.filter_by(default=True).first()
    
    def can(self,perm):
        return self.role is not None and self.role.has_permission(perm)

    def is_administrator(self):
        return self.can(Permission.ADMIN)

    def generate_forgot_password_token(self,expiration=3600):   # validity time for token is 1 hour
        s=Serializer(current_app.config['SECRET_KEY'],expiration)
        return s.dumps({'set_password':self.id}).decode('utf-8')

class AnonymousUser(AnonymousUserMixin):
    def can(self,permissions):
        return False
    def is_administrator(self):
        return False

login_manager.anonymous_user=AnonymousUser

class Consumer_request(db.Model):
    __tablename__='consumer_requests'
    id=db.Column(db.Integer,primary_key=True,index=True)
    loan_amount=db.Column(db.Integer)
    purpose=db.Column(db.String(50))
    name=db.Column(db.String(50),index=True)
    dob=db.Column(db.Date)
    gender=db.Column(db.String(6))
    pan_no=db.Column(db.String(10))
    aadhaar_no=db.Column(db.String(12))
    voter_id=db.Column(db.String(10))
    passport=db.Column(db.String(50))
    driving_license_no=db.Column(db.String(15))
    address=db.Column(db.Text(50))
    state=db.Column(db.String(50))
    pin_code=db.Column(db.Integer)
    address_category=db.Column(db.String(50))
    request_date=db.Column(db.Date,index=True)
    request_time=db.Column(db.DateTime, index=True)
    status=db.Column(db.String(15),index=True)
    remark=db.Column(db.String(100))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    consumer_report=db.relationship('Consumer_report',cascade="all,delete-orphan",backref='consumer_request',uselist=False)
    def __repr__(self):
        return '<Consumer_request %r>' % self.name

class Purpose(db.Model):
    __tablename__='purposes'
    id=db.Column(db.Integer,primary_key=True,index=True)
    purpose=db.Column(db.String(50))
    def __repr__(self):
        return self.purpose

class State(db.Model):
    __tablename__='states'
    id=db.Column(db.Integer,primary_key=True,index=True)
    state=db.Column(db.String(50))
    def __repr__(self):
        return self.state

class Address_category(db.Model):
    __tablename__='address_categories'
    id=db.Column(db.Integer,primary_key=True,index=True)
    address_category=db.Column(db.String(50))
    def __repr__(self):
        return self.address_category

class Consumer_report(db.Model):
    __tablename__='consumer_reports'
    id=db.Column(db.Integer,primary_key=True,index=True)
    uploaded_file=db.Column(db.String(255),unique=True,index=True)
    uploaded_time=db.Column(db.DateTime)
    consumer_request_id=db.Column(db.Integer,db.ForeignKey('consumer_requests.id'),unique=True,index=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))

    def __repr__(self):
        return '<Consumer_report %r>' % self.uploaded_file

class Commercial_request(db.Model):
    __tablename__='commercial_requests'
    id=db.Column(db.Integer,primary_key=True,index=True)
    name_of_unit=db.Column(db.String(50))
    constitution_type=db.Column(db.String(50))
    class_of_activity=db.Column(db.String(50))
    pan_no=db.Column(db.String(10))
    reg_office_address=db.Column(db.Text(50))
    state=db.Column(db.String(50))
    city=db.Column(db.String(20))
    pin_code=db.Column(db.Integer)
    enquiry_purpose=db.Column(db.String(50))
    member_ref_no=db.Column(db.Integer,index=True)
    loan_amount=db.Column(db.Integer)
    enquiry_type=db.Column(db.String(50))
    request_date=db.Column(db.Date,index=True)
    request_time=db.Column(db.DateTime, index=True)
    status=db.Column(db.String(15),index=True)
    remark=db.Column(db.String(100))
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    commercial_report=db.relationship('Commercial_report',cascade="all,delete-orphan",backref='commercial_request',uselist=False)

    def __repr__(self):
        return '<Commercial_request %r>' % self.name_of_unit

class Constitution_type(db.Model):
    __tablename__='constitution_types'
    id=db.Column(db.Integer,primary_key=True,index=True)
    constitution_type=db.Column(db.String(50))
    def __repr__(self):
        return self.constitution_type

class Class_of_activity(db.Model):
    __tablename__='class_of_activities'
    id=db.Column(db.Integer,primary_key=True,index=True)
    class_of_activity=db.Column(db.String(50))
    def __repr__(self):
        return self.class_of_activity

class Enquiry_purpose(db.Model):
    __tablename__='enquiry_purposes'
    id=db.Column(db.Integer,primary_key=True,index=True)
    enquiry_purpose=db.Column(db.String(50))
    def __repr__(self):
        return self.enquiry_purpose

class Enquiry_type(db.Model):
    __tablename__='enquiry_types'
    id=db.Column(db.Integer,primary_key=True,index=True)
    enquiry_type=db.Column(db.String(50))
    def __repr__(self):
        return self.enquiry_type

class Commercial_report(db.Model):
    __tablename__='commercial_reports'
    id=db.Column(db.Integer,primary_key=True,index=True)
    uploaded_file=db.Column(db.String(255),unique=True,index=True)
    uploaded_time=db.Column(db.DateTime)
    commercial_request_id=db.Column(db.Integer,db.ForeignKey('commercial_requests.id'),unique=True)
    user_id=db.Column(db.Integer,db.ForeignKey('users.id'))
    def __repr__(self):
        return '<Commercial_report %r>' % self.uploaded_file

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

