from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SelectField, PasswordField, SubmitField, RadioField,BooleanField,TextAreaField,FileField
from wtforms_sqlalchemy.fields import QuerySelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, Length, Regexp, ValidationError,EqualTo
from ..models import User, Role, Purpose, State, Address_category, Constitution_type, Class_of_activity, Enquiry_purpose, Enquiry_type

class EditProfileForm(FlaskForm):
    name=StringField('Name')
    location=StringField('Location')
    submit=SubmitField('Update')

def get_pk(obj):
    return str(obj)

def purpose_query():
    return Purpose.query

def state_query():
    return State.query

def address_category_query():
    return Address_category.query

class ConsumerForm(FlaskForm):
    loan=IntegerField('Loan amount', validators=[ DataRequired()], render_kw={'placeholder':'Enter loan amount'})
    purpose=QuerySelectField('Purpose',query_factory=purpose_query,get_pk=get_pk,allow_blank=False,get_label='purpose')
    name=StringField('Name', validators=[ DataRequired(), Length(0,64) ],render_kw={'placeholder':'Enter your name'})
    gender=RadioField('Gender', choices=[('male','Male'),('female','Female'),('others','Others')],default='male')
    dob=DateField('Date of birth', validators=[ DataRequired()], format='%Y-%m-%d' )
    pan=StringField('PAN No.',validators=[ DataRequired()],render_kw={'placeholder':'Enter your PAN Number'})
    aadhaar=IntegerField('Aadhaar No.',render_kw={'placeholder':'Enter your Aadhaar Number if any'})
    voter_id=StringField('Voter Id.',render_kw={'placeholder':'Enter your Voter ID if any'})
    passport=StringField('Paassport',render_kw={'placeholder':'Enter your Passport Number if any'})
    driving_lic=StringField('Driving License',render_kw={'placeholder':'Enter your Driving License Number if any'})
    address=StringField('Address',validators=[ DataRequired(), Length(0,50) ],render_kw={'placeholder':'Enter your address'})
    state=QuerySelectField('State',query_factory=state_query,get_pk=get_pk,allow_blank=False,get_label='state')
    pin=IntegerField('Pin code',validators=[ DataRequired()],render_kw={'placeholder':'Enter pin code'})
    address_category=QuerySelectField('Address Category',query_factory=address_category_query,get_pk=get_pk,allow_blank=False,get_label='address_category')
    submit=SubmitField('Submit')

def constitution_query():
    return Constitution_type.query

def activity_query():
    return Class_of_activity.query

def enquiry_purpose_query():
    return Enquiry_purpose.query

def enquiry_type_query():
    return Enquiry_type.query

class CommercialForm(FlaskForm):
    unit=StringField('Name of the Unit', validators=[ DataRequired(),Length(0,64) ],render_kw={'placeholder':'Enter name of the Unit'})
    constitution=QuerySelectField('Constitution Type',query_factory=constitution_query,get_pk=get_pk,allow_blank=False,get_label='constitution_type')
    activity=QuerySelectField('Class of Activity',query_factory=activity_query,get_pk=get_pk,allow_blank=False,get_label='class_of_activity')
    pan=StringField('PAN No.',validators=[ DataRequired(),Length(0,10) ],render_kw={'placeholder':'Enter your PAN Number'})
    address=StringField('Registered Office Address',validators=[ DataRequired(),Length(0,50) ],render_kw={'placeholder':'Enter your address'})
    state=QuerySelectField('State',query_factory=state_query,get_pk=get_pk,allow_blank=False,get_label='state')
    city=StringField('City',validators=[DataRequired(),Length(0,50) ],render_kw={'placeholder':'Enter your city'})
    pin=IntegerField('Pin code',validators=[ DataRequired() ],render_kw={'placeholder':'Enter pin code'})
    enquiry_purpose=QuerySelectField('Enquiry_purpose',query_factory=enquiry_purpose_query,get_pk=get_pk,allow_blank=False,get_label='enquiry_purpose')
    ref_no=StringField('Member Reference No.',validators=[ DataRequired(),Length(0,10) ],render_kw={'placeholder':'Enter Member Reference No.'})
    loan=IntegerField('Loan amount',validators=[ DataRequired()],render_kw={'placeholder':'Enter loan amount'})
    enquiry_type=QuerySelectField('Enquiry_type',query_factory=enquiry_type_query,get_pk=get_pk,allow_blank=False,get_label='enquiry_type')
    submit=SubmitField('Submit')

class ConsumerReport(FlaskForm):
    date=DateField('Reports by date')
    submit=SubmitField('Search')

class CommercialReport(FlaskForm):
    date=DateField('Reports by date')
    submit=SubmitField('Search')

class ConsumerRequestSearchForm(FlaskForm):
    search_name=StringField('Cibil report for',render_kw={'placeholder':'Search here'})
    from_date=DateField('From date')
    to_date=DateField('To date')
    status=SelectField(u'Status',choices=[('Pending','Pending'),('Completed','Completed'),('Returned','Returned'),('Rejected','Rejected')])
    submit=SubmitField('Search')

class CommercialRequestSearchForm(FlaskForm):
    unit_name=StringField('Unit Name',render_kw={'placeholder':'Search here'})
    pan_no=StringField('PAN No.',render_kw={'placeholder':'Search here'})
    from_date=DateField('From date')
    to_date=DateField('To date')
    status=SelectField(u'Status',choices=[('Pending','Pending'),('Completed','Completed'),('Returned','Returned'),('Rejected','Rejected')])
    submit=SubmitField('Search')

class UserSearchConsumerRequestByNameForm(FlaskForm):
    search_name=StringField('Search by Requester name')
    submit=SubmitField('Search')

class UserSearchConsumerRequestByDateForm(FlaskForm):
    search_date=DateField('Search by date')
    submit=SubmitField('Search')

class UserSearchCommercialRequestByNameForm(FlaskForm):
    search_name=StringField('Search by name')
    submit=SubmitField('Search')

class UserSearchCommercialRequestByDateForm(FlaskForm):
    search_date=DateField('Search by date')
    submit=SubmitField('Search')

class UserResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')],render_kw={'placeholder':'Enter password'})
    password2=PasswordField('Confirm password',validators=[DataRequired()],render_kw={'placeholder':'Confirm password'})
    submit=SubmitField('Submit')

class AdminEditUserProfileForm(FlaskForm):
    email=StringField('Email',validators=[ DataRequired(), Length(1,64),Email()])
    username=StringField('Username',validators=[ DataRequired(), Length(1,64), Regexp('^[A-Za-z0-9_.]*$',0,'Usernames must have only letters, numbers, dots or underscores ') ])
    name=StringField('Name')
    role=RadioField('Role',coerce=int)
    location=StringField('Location')
    submit=SubmitField('Submit')
    
    def __init__(self,user,*args,**kwargs):
        super(AdminEditUserProfileForm,self).__init__(*args,**kwargs)
        self.role.choices=[(role.id, role.name) for role in Role.query.filter(Role.name!="Admin").all()]
        self.user=user
    
    #def validate_email(self,field):
        #if field.data!=self.user.email and User.query.filter_by(email=field.data).first():
            #raise ValidationError('Email already registered.')
   
    #def validate_email(self,field):
        #if User.query.filter_by(email=field.data).first():
            #raise ValidationError('Email already registered.')

    #def validate_username(self,field):
        #if User.query.filter_by(username=field.data).first():
           #raise ValidationError('Username already in use.')

class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[ DataRequired(), Length(1,50), Email() ],render_kw={'placeholder':'Enter your email'})
    username=StringField('Username',validators=[DataRequired(), Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores') ],render_kw={'placeholder':'Enter a username'})
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')],render_kw={'placeholder':'Enter password'})
    password2=PasswordField('Confirm password',validators=[DataRequired()],render_kw={'placeholder':'Confirm password'})
    submit=SubmitField('Create')

class DeleteUserForm(FlaskForm):
    yes_no=RadioField('', choices=[('yes','Yes'),('no','No')])
    submit = SubmitField('Submit')

class UploadConsumerFileForm(FlaskForm):
    report=FileField('Upload file')
    submit=SubmitField('Submit')
    reject=SubmitField('Reject')

class AdminConsumerRequestSearchForm(FlaskForm):
    search_username=StringField('Requested by',render_kw={'placeholder':'Search here'})
    search_name=StringField('Cibil report for',render_kw={'placeholder':'Search here'})
    from_date=DateField('From date')
    to_date=DateField('To date')
    status=SelectField(u'Status',choices=[('Pending','Pending'),('Completed','Completed'),('Returned','Returned'),('Rejected','Rejected')])
    submit=SubmitField('Search')

class AdminCommercialRequestSearchForm(FlaskForm):
    username=StringField('Requested by',render_kw={'placeholder':'Search here'})
    unit_name=StringField('Unit Name',render_kw={'placeholder':'Search here'})
    pan_no=StringField('PAN No.',render_kw={'placeholder':'Search here'})
    from_date=DateField('From date')
    to_date=DateField('To date')
    status=SelectField(u'Status',choices=[('Pending','Pending'),('Completed','Completed'),('Returned','Returned'),('Rejected','Rejected')])
    submit=SubmitField('Search')

class AdminSearchUserForm(FlaskForm):
    name=StringField('Username',render_kw={'placeholder':'Search here'})
    submit=SubmitField('Search')

class SearchConsumerRequestByNameForm(FlaskForm):
    name=StringField('Search by requester name')
    submit=SubmitField('Search')

class SearchConsumerRequestByUsernameForm(FlaskForm):
    username=StringField('Search by username')
    submit=SubmitField('Search')

class SearchConsumerRequestByDateForm(FlaskForm):
    date=DateField('Search by date')
    submit=SubmitField('Search')

class AdminEditProfileForm(FlaskForm):
    name=StringField('Name')
    location=StringField('Location')
    about_me=TextAreaField('About me')
    submit=SubmitField('Update')

class AdminResetPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')],render_kw={'placeholder':'Enter password'})
    password2=PasswordField('Confirm password',validators=[DataRequired()],render_kw={'placeholder':'Confirm password'})
    submit=SubmitField('Submit')

class ReturnRemarkForm(FlaskForm):
    remark=TextAreaField('Remark')
    return_req=SubmitField('Return')


