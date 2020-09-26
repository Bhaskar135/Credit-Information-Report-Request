from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField, RadioField, SubmitField
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User

class LoginForm(FlaskForm):
    email=StringField('Email Address',validators=[ DataRequired(), Length(1,50), Email() ],render_kw={'placeholder':'Enter your email'})
    password=PasswordField('Password',validators=[ DataRequired() ],render_kw={'placeholder':'Enter Password'})
    remember_me=BooleanField('Keep me logged in')
    submit=SubmitField('Log In')

class RegistrationForm(FlaskForm):
    email=StringField('Email',validators=[ DataRequired(), Length(1,50), Email() ],render_kw={'placeholder':'Enter your email'})
    username=StringField('Username',validators=[DataRequired(), Length(1,64),Regexp('^[A-Za-z][A-Za-z0-9_.]*$',0,'Usernames must have only letters,numbers,dots or underscores') ],render_kw={'placeholder':'Enter a username'})
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')],render_kw={'placeholder':'Enter password'})
    password2=PasswordField('Confirm password',validators=[DataRequired()],render_kw={'placeholder':'Confirm password'})
    submit=SubmitField('Register')
    
    #def validate_email(self,field):
        #if User.query.filter_by(email=field.data).first():
            #raise ValidationError('Email already registered.')
    
    #def validate_username(self,field):
        #if User.query.filter_by(username=field.data).first():
            #raise ValidationError('Username already registered.')

class ForgotPasswordForm(FlaskForm):
    email=StringField('We will send a link to your email account.',validators=[ DataRequired(), Length(1,50), Email() ],render_kw={'placeholder':'Enter your email'})    
    submit=SubmitField('Submit')

class ResetForgotPasswordForm(FlaskForm):
    password=PasswordField('Password',validators=[DataRequired(),EqualTo('password2',message='Passwords must match.')],render_kw={'placeholder':'Enter password'})
    password2=PasswordField('Confirm password',validators=[DataRequired()],render_kw={'placeholder':'Confirm password'})
    submit=SubmitField('Submit')


