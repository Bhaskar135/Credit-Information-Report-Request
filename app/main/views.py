from datetime import datetime, date
from flask import render_template, session, redirect, url_for, flash, current_app, request, make_response
from .import main
from ..import db
from ..models import Permission, User, Role, Purpose, State, Address_category, Consumer_request, Consumer_report, Commercial_request, Constitution_type, Class_of_activity, Enquiry_purpose, Enquiry_type, Commercial_report
from .forms import UserResetPasswordForm, ConsumerRequestSearchForm, CommercialRequestSearchForm, EditProfileForm, UserSearchConsumerRequestByNameForm, UserSearchConsumerRequestByDateForm, ConsumerForm, CommercialForm, ConsumerReport, CommercialReport
from .forms import AdminEditProfileForm, RegistrationForm, AdminResetPasswordForm, DeleteUserForm, AdminConsumerRequestSearchForm, AdminCommercialRequestSearchForm, SearchConsumerRequestByNameForm, SearchConsumerRequestByUsernameForm, SearchConsumerRequestByDateForm, AdminSearchUserForm, AdminEditUserProfileForm, UploadConsumerFileForm, ReturnRemarkForm
from flask_login import current_user
from app.auth.forms import LoginForm
from flask_login import login_required
from ..decorators import admin_required
from werkzeug.utils import secure_filename
import os
import pdfkit

# ..........................Users coding part....................................


@main.route('/', methods=['GET', 'POST'])
def home():
    '''
    Home page and consumer request page.
    Also search consumer requests by name or date
    '''
    form1 = ConsumerRequestSearchForm()
    if current_user.is_authenticated:
        if current_user.is_administrator():
            return redirect(url_for('main.admin_home'))
        elif current_user.role_id == 2:
            return redirect(url_for('main.report_admin_home'))
        page = request.args.get('page', 1, type=int)
        if request.args.get('search_name') and request.args.get('from_date') and request.args.get('to_date'):
            search_value1 = request.args.get('search_name')
            search_value2 = request.args.get('from_date')
            search_value3 = request.args.get('to_date')
            search_value4 = request.args.get('status')
            form1.status.data = request.args.get('status')
            consumer_requests = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value4}'+'%')).order_by(Consumer_request.request_time.desc())      
            return render_template('home.html', consumer_requests=consumer_requests, form1=form1)
        elif request.args.get('search_name') and request.args.get('from_date'):
            search_value1 = request.args.get('search_name')
            search_value2 = request.args.get('from_date')
            search_value3 = datetime.today()
            search_value4 = request.args.get('status')
            form1.status.data = request.args.get('status')
            consumer_requests = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value4}'+'%')).order_by(Consumer_request.request_time.desc())      
            return render_template('home.html', consumer_requests=consumer_requests, form1=form1)
        elif request.args.get('from_date') and request.args.get('to_date'):
            search_value1 = request.args.get('from_date')
            search_value2 = request.args.get('to_date')
            search_value3 = request.args.get('status')
            form1.status.data = request.args.get('status')
            consumer_requests = Consumer_request.query.filter(Consumer_request.request_date.between(search_value1, search_value2)).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())      
            return render_template('home.html', consumer_requests=consumer_requests, form1=form1)
        elif request.args.get('search_name'):
            search_value1 = request.args.get('search_name')
            search_value2 = request.args.get('status')
            form1.status.data = request.args.get('status')
            consumer_requests = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.status.like('%'+f'{search_value2}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('home.html', consumer_requests=consumer_requests, form1=form1)
        elif request.args.get('from_date'):
            search_value1 = request.args.get('from_date')
            search_value2 = date.today()
            search_value3 = request.args.get('status')
            form1.status.data = request.args.get('status')
            consumer_requests = Consumer_request.query.filter(Consumer_request.request_date.between(search_value1, search_value2)).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('home.html', consumer_requests=consumer_requests, form1=form1)
        elif request.args.get('status'):
            search_value1 = request.args.get('status')
            form1.status.data = request.args.get('status')
            consumer_requests = Consumer_request.query.filter(Consumer_request.status.like('%'+f'{search_value1}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('home.html', consumer_requests=consumer_requests, form1=form1)
        else:
            pagination=Consumer_request.query.filter_by(user_id=current_user.id).filter_by(status="Pending").order_by(Consumer_request.request_time.desc()).paginate(page , per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_req = pagination.items
        return render_template('home.html', page=page, consumer_req=consumer_req, pagination=pagination, form1=form1)
    else:
        return redirect(url_for('auth.login'))

@main.route('/commercial-requests')
@login_required
def commercial_requests():
    '''
    Commercial requests page
    '''
    form = CommercialRequestSearchForm()
    page = request.args.get('page', 1, type=int)
    if request.args.get('unit_name') and request.args.get('pan_no') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('from_date')
        search_value4 = request.args.get('to_date')
        search_value5 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.request_date.between(search_value3,search_value4)).filter(Commercial_request.status.like('%'+f'{search_value5}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('unit_name') and request.args.get('pan_no') and request.args.get('from_date'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('from_date')
        search_value4 = date.today()
        search_value5 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.request_date.between(search_value3,search_value4)).filter(Commercial_request.status.like('%'+f'{search_value5}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('unit_name') and request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('pan_no') and request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('pan_no')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('unit_name') and request.args.get('pan_no'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('unit_name') and request.args.get('from_date'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('pan_no') and request.args.get('from_date'):
        search_value1 = request.args.get('pan_no')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('from_date')
        search_value2 = request.args.get('to_date')
        search_value3 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.request_date.between(search_value1,search_value2)).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('unit_name'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value2}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('pan_no'):
        search_value1 = request.args.get('pan_no')
        search_value2 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value2}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('from_date'):
        search_value1 = request.args.get('from_date')
        search_value2 = date.today()
        search_value3 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.request_date.between(search_value1,search_value2)).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('status'):
        search_value1 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.status.like('%'+f'{search_value1}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('commercial_requests.html', form=form, commercial_requests=commercial_requests)
    pagination = Commercial_request.query.filter_by(user_id=current_user.id).filter_by(status="Pending").order_by(Commercial_request.request_time.desc()).paginate(page , per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
    commercial_req = pagination.items
    return render_template('commercial_requests.html', form=form, commercial_req=commercial_req, pagination=pagination, page=page)


@main.route('/user/<username>')
def user(username):
    '''
    Profile page of the User
    '''
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('profile.html', user=user)

@main.route('/user/<username>/edit-profile', methods=['GET', 'POST'])
@login_required
def edit_profile(username):
    '''
    Edit profile of the user page
    '''
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated successfully..')
        return redirect(url_for('.user', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    return render_template('edit_profile.html', form=form)

@main.route('/user/<username>/consumer-form', methods=['GET', 'POST'])
@login_required
def consumer_form(username):
    '''
    consumer request form
    '''
    form = ConsumerForm()
    if current_user.can(Permission.WRITE) and request.method == "POST":
        loan = form.loan.data
        purpose = str(form.purpose.data)
        name = form.name.data
        gender = form.gender.data
        dob = form.dob.data
        pan = form.pan.data
        aadhaar = form.aadhaar.data
        voter_id = form.voter_id.data
        passport = form.passport.data
        driving_lic = form.driving_lic.data
        address = form.address.data
        state = str(form.state.data)
        pin = form.pin.data
        address_category= str(form.address_category.data)
        status = "Pending"
        consumer_req = Consumer_request(name=name, purpose=purpose, gender=gender,dob=dob,loan_amount=loan,pan_no=pan,aadhaar_no=aadhaar,voter_id=voter_id,passport=passport,driving_license_no=driving_lic,address=address,state=state,pin_code=pin, address_category=address_category, request_date=date.today(),request_time=datetime.now(),status=status,user=current_user._get_current_object())
        db.session.add(consumer_req)
        db.session.commit()
        flash("Your consumer request has been sent successfully..")
        return redirect(url_for('.consumer_request_detail',request_id=consumer_req.id))
    return render_template('consumer-form.html', form=form , username=username)

@main.route('/user/<username>/consumer-form/edit', methods=['GET', 'POST'])
@login_required
def consumer_form_edit(username):
    '''
    consumer request edit form
    '''
    form = ConsumerForm()
    user = User.query.filter_by(username=current_user.username).first()
    request_id = request.args.get('request_id')
    consumer_request = user.consumer_requests.filter_by(id=request_id).first()
    if current_user.can(Permission.WRITE) and request.method == "POST":
        consumer_request.loan_amount = form.loan.data
        consumer_request.purpose = str(form.purpose.data)
        consumer_request.name = form.name.data
        consumer_request.dob = form.dob.data
        consumer_request.gender = form.gender.data
        consumer_request.pan_no = form.pan.data
        consumer_request.aadhaar_no = form.aadhaar.data
        consumer_request.voter_id = form.voter_id.data
        consumer_request.passport = form.passport.data
        consumer_request.driving_license_no = form.driving_lic.data
        consumer_request.address = form.address.data
        consumer_request.state = str(form.state.data)
        consumer_request.pin_code = form.pin.data
        consumer_request.address_category = str(form.address_category.data)
        consumer_request.status = "Pending"
        consumer_request.remark = ""
        db.session.add(consumer_request)
        db.session.commit()
        flash("Your consumer request has been sent successfully..")
        return redirect(url_for('.consumer_request_detail', username=username,request_id=request_id))
    form.loan.data = consumer_request.loan_amount
    form.purpose.data=consumer_request.purpose
    form.name.data = consumer_request.name
    form.dob.data = consumer_request.dob
    form.gender.data = consumer_request.gender
    form.pan.data = consumer_request.pan_no
    form.aadhaar.data = consumer_request.aadhaar_no
    form.voter_id.data = consumer_request.voter_id
    form.passport.data = consumer_request.passport
    form.driving_lic.data = consumer_request.driving_license_no
    form.address.data = consumer_request.address
    form.state.data = consumer_request.state
    form.pin.data = consumer_request.pin_code
    form.address_category.data=consumer_request.address_category
    return render_template('consumer-form-edit.html', form=form, username=username, request_id=request_id)


@main.route('/user/<username>/commercial-form', methods=['GET', 'POST'])
@login_required
def commercial_form(username):
    '''
    commercial request form
    '''
    form = CommercialForm()
    if current_user.can(Permission.WRITE) and request.method == "POST":
        name_of_unit = form.unit.data
        constitution_type = str(form.constitution.data)
        class_of_activity = str(form.activity.data)
        pan_no = form.pan.data
        address = form.address.data
        state = str(form.state.data)
        city = form.city.data
        pin_code = form.pin.data
        enquiry_purpose = str(form.enquiry_purpose.data)
        ref_no=form.ref_no.data
        loan_amount = form.loan.data
        enquiry_type = str(form.enquiry_type.data)
        status="Pending"
        commercial_req = Commercial_request(name_of_unit=name_of_unit,constitution_type=constitution_type,class_of_activity=class_of_activity, pan_no=pan_no,reg_office_address=address,state=state,city=city,pin_code=pin_code,enquiry_purpose=enquiry_purpose,member_ref_no=ref_no,loan_amount=loan_amount,enquiry_type=enquiry_type,request_date=date.today(),request_time=datetime.now(),status=status,user=current_user._get_current_object())
        db.session.add(commercial_req)
        db.session.commit()
        return redirect(url_for('.commercial_request_detail',request_id=commercial_req.id))
    return render_template('commercial-form.html', form=form, username=username)

@main.route('/user/<username>/commercial-form/edit', methods=['GET', 'POST'])
@login_required
def commercial_form_edit(username):
    form = CommercialForm()
    user = User.query.filter_by(username=current_user.username).first()
    request_id = request.args.get('request_id')
    commercial_request = user.commercial_requests.filter_by(id=request_id).first()
    if current_user.can(Permission.WRITE) and request.method == "POST":
        commercial_request.name_of_unit=form.unit.data
        commercial_request.constitution_type=str(form.constitution.data)
        commercial_request.class_of_activity=str(form.activity.data)
        commercial_request.pan_no=form.pan.data
        commercial_request.reg_office_address=form.address.data
        commercial_request.state=str(form.state.data)
        commercial_request.city=form.city.data
        commercial_request.pin_code=form.pin.data
        commercial_request.enquiry_purpose=str(form.enquiry_purpose.data)
        commercial_request.member_ref_no=form.ref_no.data
        commercial_request.loan_amount = form.loan.data
        commercial_request.enquiry_type=str(form.enquiry_type.data)
        commercial_request.status="Pending"
        commercial_request.remark = ""
        db.session.add(commercial_request)
        db.session.commit()
        return redirect(url_for('main.commercial_request_detail',username=username,request_id=request_id))
    form.unit.data=commercial_request.name_of_unit
    form.constitution.data=commercial_request.constitution_type
    form.activity.data=commercial_request.class_of_activity
    form.pan.data=commercial_request.pan_no
    form.address.data=commercial_request.reg_office_address
    form.state.data=commercial_request.state
    form.city.data=commercial_request.city
    form.pin.data=commercial_request.pin_code
    form.enquiry_purpose.data=commercial_request.enquiry_purpose
    form.ref_no.data=commercial_request.member_ref_no
    form.loan.data = commercial_request.loan_amount
    form.enquiry_type.data=commercial_request.enquiry_type
    return render_template('commercial-form-edit.html', form=form, username=username, request_id=request_id)

@main.route('/consumer-request')
@login_required
def consumer_request_detail():
    '''
    This will show the details of a consumer request 
    '''
    user = User.query.filter_by(username=current_user.username).first()
    request_id = request.args.get('request_id')
    consumer_request_id = user.consumer_requests.filter_by(id=request_id).first()
    consumer_report_id = consumer_request_id.consumer_report
    return render_template('consumer_request_detail.html', consumer_request_id=consumer_request_id, consumer_report_id=consumer_report_id,user=user)

@main.route('/commercial-request')
@login_required
def commercial_request_detail():
    '''
    This will show the details of a commercial request 
    '''
    user = User.query.filter_by(username=current_user.username).first()
    request_id = request.args.get('request_id')
    commercial_request_id = user.commercial_requests.filter_by(id=request_id).first()
    commercial_report_id = commercial_request_id.commercial_report
    return render_template('commercial_request_detail.html', commercial_request_id=commercial_request_id, commercial_report_id=commercial_report_id,user=user)

@main.route('/user/<username>/reset_password', methods=["GET", "POST"])
def user_reset_password(username):
    '''
    User can change his password
    '''
    form = UserResetPasswordForm()
    user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash("Your password has been changed successfully..")
        return redirect(url_for('main.user', username=username))
    return render_template('user_reset_password.html', form=form)

# .....................Admin coding part......................................

@main.route('/admin', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_home():
    '''
    showing admin home page.
    admin can search users by username.
    admin can delete users.
    '''
    form = AdminSearchUserForm()
    if request.args.get('name'):
        name = request.args.get('name')
        user = User.query.filter(User.username.like('%'+f'{name}'+'%')).order_by(User.username).all()
        if user:
            pass
        else:
            flash('User does not exist.')
            return redirect(url_for('main.admin_home', form=form, user=user))
    else:
        if request.method == 'POST':
            if request.form.getlist('usercheckbox') != []:
                for username in request.form.getlist('usercheckbox'):
                    user = User.query.filter_by(username=username).first()
                    consumer_requests = user.consumer_requests.all()
                    for requests in consumer_requests:
                        db.session.delete(requests)
                        db.session.commit()
                    db.session.delete(user)
                    db.session.commit()
        user = User.query.filter(User.role_id != 3).order_by(User.username).all()
    return render_template('admin_home.html', form=form, user=user)

@main.route('/admin/create_user',methods=['GET','POST'])
@login_required
@admin_required
def admin_create_user():
    form=RegistrationForm()
    if form.validate_on_submit():
        if User.query.filter_by(email=form.email.data).first():
            flash('Email already registered.')
            return redirect(url_for('auth.register'))
        elif User.query.filter_by(username=form.username.data).first():
            flash('Username already registered.')
            return redirect(url_for('auth.register'))
        else:
            user=User(email=form.email.data,username=form.username.data,password=form.password.data)
            db.session.add(user)
            db.session.commit()
            return redirect(url_for('main.admin_home'))
    return render_template('admin_create_user.html',form=form)

@main.route('/admin/consumer-requests')
@login_required
@admin_required
def all_users_consumer_requests():
    '''
    showing all consumer requests.
    search consumer requests by name 
    search consumer requests by username 
    search consumer requests by date 
    '''
    form = AdminConsumerRequestSearchForm()
    page = request.args.get('page', 1, type=int)
    if request.args.get('search_name') and request.args.get('search_username') and request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('search_name')
        search_value3 = request.args.get('from_date')
        search_value4 = request.args.get('to_date')
        search_value5 = request.args.get('status')
        form.status.data = search_value5
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.request_date.between(search_value3, search_value4)).filter(Consumer_request.status.like('%'+f'{search_value5}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.all_users_consumer_requests'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.request_date.between(search_value3, search_value4)).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name') and request.args.get('search_username') and request.args.get('from_date'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('search_name')
        search_value3 = request.args.get('from_date')
        search_value4 = date.today()
        search_value5 = request.args.get('status')
        form.status.data = search_value5
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.request_date.between(search_value3, search_value4)).filter(Consumer_request.status.like('%'+f'{search_value5}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.all_users_consumer_requests'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.request_date.between(search_value3, search_value4)).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_username') and request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value4}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.all_users_consumer_requests'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.request_date.between(search_value2, search_value3)).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name') and request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('search_name')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        consumer_req = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value4}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
    elif request.args.get('search_name') and request.args.get('search_username'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('search_name')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.all_users_consumer_requests'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_username') and request.args.get('from_date'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.all_users_consumer_requests'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.request_date.between(search_value2, search_value3)).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name') and request.args.get('from_date'):
        search_value1 = request.args.get('search_name')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        consumer_req = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value4}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
    elif request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('from_date')
        search_value2 = request.args.get('to_date')
        search_value3 = request.args.get('status')
        form.status.data=search_value3
        consumer_req = Consumer_request.query.filter(Consumer_request.request_date.between(search_value1, search_value2)).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
    elif request.args.get('search_username'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('status')
        form.status.data=search_value2
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.status.like('%'+f'{search_value2}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.all_users_consumer_requests'))
        # consumer_req = user.consumer_requests.order_by(Consumer_request.request_time.desc())
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name'):
        search_value1 = request.args.get('search_name')
        search_value2 = request.args.get('status')
        form.status.data = search_value2
        consumer_req = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.status.like('%'+f'{search_value2}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
    elif request.args.get('from_date'):
        search_value1 = request.args.get('from_date')
        search_value2 = date.today()
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        consumer_req = Consumer_request.query.filter(Consumer_request.request_date.between(search_value1, search_value2)).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
    elif request.args.get('status'):
        search_value1 = request.args.get('status')
        form.status.data = search_value1
        consumer_req = Consumer_request.query.filter(Consumer_request.status.like('%'+f'{search_value1}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('admin_all_users_consumer_requests.html', form=form,consumer_req=consumer_req)
    else:
        pagination = Consumer_request.query.filter_by(status="Pending").order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
        consumer_requests = pagination.items
    return render_template('admin_all_users_consumer_requests.html', form=form,consumer_requests=consumer_requests,pagination=pagination,page=page)

@main.route('/admin/commercial-requests')
@login_required
@admin_required
def all_users_commercial_requests():
    '''
    showing all commercial requests.
    '''
    form=AdminCommercialRequestSearchForm()
    page = request.args.get('page', 1, type=int)
    if request.args.get('username') and request.args.get('unit_name') and request.args.get('pan_no') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('pan_no')
        search_value4 = request.args.get('from_date')
        search_value5 = request.args.get('to_date')
        search_value6 = request.args.get('status') 
        form.status.data = search_value6
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.request_date.between(search_value4,search_value5)).filter(Commercial_request.status.like('%'+f'{search_value6}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.request_date.between(search_value4,search_value5)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('unit_name') and request.args.get('pan_no') and request.args.get('from_date') :
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('pan_no')
        search_value4 = request.args.get('from_date')
        search_value5 = date.today()
        search_value6 = request.args.get('status')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.request_date.between(search_value4,search_value5)).filter(Commercial_request.status.like('%'+f'{search_value6}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.request_date.between(search_value4,search_value5)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('unit_name') and request.args.get('pan_no'):
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('pan_no')
        search_value4 = request.args.get('status')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value6}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('unit_name') and request.args.get('from_date') :
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('from_date')
        search_value4 = date.today()
        search_value5 = request.args.get('status')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.request_date.between(search_value3,search_value4)).filter(Commercial_request.status.like('%'+f'{search_value5}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.request_date.between(search_value3,search_value4)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.request_date.between(search_value2,search_value3)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('unit_name') and request.args.get('pan_no') and request.args.get('from_date'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('from_date')
        search_value4 = date.today()
        search_value5 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.request_date.between(search_value3,search_value4)).filter(Commercial_request.status.like('%'+f'{search_value5}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('unit_name') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('pan_no') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('pan_no')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        commercial_requests = user.commercial_requests.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('username') and request.args.get('unit_name'):
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('pan_no'):
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('from_date'):
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.request_date.between(search_value2,search_value3)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('unit_name') and request.args.get('pan_no') :
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('unit_name') and request.args.get('from_date'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('pan_no') and request.args.get('from_date'):
        search_value1 = request.args.get('pan_no')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        commercial_requests = user.commercial_requests.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('from_date')
        search_value2 = request.args.get('to_date')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        commercial_requests = Commercial_request.query.filter(Commercial_request.request_date.between(search_value1,search_value2)).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('username') :
        search_value1 = request.args.get('username')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).order_by(Commercial_request.request_time.desc())
            return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.all_users_commercial_requests'))
        # commercial_requests = user.commercial_requests.order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('unit_name'):
        search_value1 = request.args.get('unit_name')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('pan_no') :
        search_value1 = request.args.get('pan_no')
        commercial_requests = Commercial_request.query.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('from_date'):
        search_value1 = request.args.get('from_date')
        search_value2 = date.today()
        commercial_requests = Commercial_request.query.filter(Commercial_request.request_date.between(search_value1,search_value2)).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    elif request.args.get('status'):
        search_value1=request.args.get('status')
        form.status.data=search_value1
        commercial_requests = Commercial_request.query.filter_by(status=search_value1).order_by(Commercial_request.request_time.desc())
        return render_template('admin_all_users_commercial_requests.html', form=form, commercial_requests=commercial_requests)
    pagination = Commercial_request.query.filter_by(status="Pending").order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
    commercial_req = pagination.items
    return render_template('admin_all_users_commercial_requests.html', form=form, commercial_req=commercial_req,pagination=pagination,page=page)

@main.route('/admin/consumer-form', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_consumer_form():
    '''
    consumer request form
    '''
    form = ConsumerForm()
    if current_user.can(Permission.WRITE) and current_user.can(Permission.ADMIN) and request.method == "POST":
        loan = form.loan.data
        purpose = str(form.purpose.data)
        name = form.name.data
        gender = form.gender.data
        dob = form.dob.data
        pan = form.pan.data
        aadhaar = form.aadhaar.data
        voter_id = form.voter_id.data
        passport = form.passport.data
        driving_lic = form.driving_lic.data
        address = form.address.data
        state = str(form.state.data)
        pin = form.pin.data
        address_category= str(form.address_category.data)
        status = "Pending"
        consumer_req = Consumer_request(name=name, purpose=purpose, gender=gender,dob=dob,loan_amount=loan,pan_no=pan,aadhaar_no=aadhaar,voter_id=voter_id,passport=passport,driving_license_no=driving_lic,address=address,state=state,pin_code=pin, address_category=address_category, request_date=date.today(),request_time=datetime.now(),status=status,user=current_user._get_current_object())
        db.session.add(consumer_req)
        db.session.commit()
        flash("Your consumer request has been sent successfully..")
        return redirect(url_for('.all_users_consumer_requests'))
    return render_template('admin-consumer-form.html', form=form)

@main.route('/admin/commercial-form', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_commercial_form():
    '''
    commercial request form
    '''
    form = CommercialForm()
    if current_user.can(Permission.WRITE) and current_user.can(Permission.ADMIN) and request.method == "POST":
        name_of_unit = form.unit.data
        constitution_type = str(form.constitution.data)
        class_of_activity = str(form.activity.data)
        pan_no = form.pan.data
        address = form.address.data
        state = str(form.state.data)
        city = form.city.data
        pin_code = form.pin.data
        enquiry_purpose = str(form.enquiry_purpose.data)
        ref_no=form.ref_no.data
        loan_amount = form.loan.data
        enquiry_type = str(form.enquiry_type.data)
        status="Pending"
        commercial_req = Commercial_request(name_of_unit=name_of_unit,constitution_type=constitution_type,class_of_activity=class_of_activity, pan_no=pan_no,reg_office_address=address,state=state,city=city,pin_code=pin_code,enquiry_purpose=enquiry_purpose,member_ref_no=ref_no,loan_amount=loan_amount,enquiry_type=enquiry_type,request_date=date.today(),request_time=datetime.now(),status=status,user=current_user._get_current_object())
        db.session.add(commercial_req)
        db.session.commit()
        flash("Your commercial request has been sent successfully..")
        return redirect(url_for('.all_users_commercial_requests'))
    return render_template('admin-commercial-form.html', form=form)

def allowed_file(filename):
    if not '.' in filename:
        print('Not . in filename')
        return False
    ext = filename.rsplit('.', 1)[1]
    if ext.lower() in current_app.config['ALLOWED_FILE_EXTENSIONS']:
        return True
    else:
        return False

@main.route('/admin/users/<username>/consumer-request', methods=['GET', 'POST'])
@login_required
@admin_required
def user_consumer_request_detail(username):
    '''
    admin can see users consumer requests and upload file against the requests.
    '''
    form = UploadConsumerFileForm()
    form2 = ReturnRemarkForm()
    user = User.query.filter_by(username=username).first()
    request_id = request.args.get('request_id')
    user_request = user.consumer_requests.filter_by(id=request_id).first()
    consumer_file = user_request.consumer_report    # to get the uploaded consumer file
    if form2.validate_on_submit() and form2.return_req.data:
        if user_request.status=="Pending":
            user_request.status = "Returned"
            user_request.remark = form2.remark.data
            db.session.commit()
        else:
            flash("The request is already "+user_request.status)
        return redirect(url_for('main.user_consumer_request_detail',username=username,request_id=request_id))
    if form.validate_on_submit() and form.submit.data or form.reject.data:
        if user_request.status=="Pending":
            if form.submit.data:
                report = request.files['report']
                if report.filename == "":
                    flash('No file is selected.')
                    return redirect(url_for('main.user_consumer_request_detail',username=username,request_id=request_id))
                filename = secure_filename(report.filename)
                if user_request.consumer_report:
                    flash("File is already uploaded..")
                    return redirect(url_for('main.user_consumer_request_detail',username=username,request_id=request_id))
                else:
                    if allowed_file(report.filename):
                        part1 = filename.split('.')
                        today_date_with_slace=str(date.today().strftime('%d-%m-%Y'))
                        today_date_array=today_date_with_slace.split('-')
                        today_date=''
                        for getdate in today_date_array:
                            today_date=today_date+getdate
                        name_with_white_space=user_request.name.split(' ')
                        full_name=''
                        for name in name_with_white_space:
                            full_name=full_name+name
                        part1[0]=full_name+'_consumer_'+today_date
                        new_filename = part1[0] + '.' + part1[1]
                        consumer_report = Consumer_report(uploaded_file=new_filename, uploaded_time=datetime.now(), consumer_request_id=request_id, user_id=user.id)                
                        db.session.add(consumer_report)
                        db.session.commit()
                        report.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
                        consumer_req = Consumer_request.query.filter_by(id=request_id).first()
                        consumer_req.status = "Completed"
                        db.session.commit()
                        return redirect(url_for('main.user_consumer_request_detail', username=username,request_id=request_id))
                    else:
                        return redirect(url_for('main.user_consumer_request_detail', username=username,request_id=request_id))
            elif form.reject.data:
                user_request.status="Rejected"
                db.session.commit()
                flash("Rejected the request.")
                return redirect(url_for('main.user_consumer_request_detail',username=username,request_id=request_id))
        else:
            flash("The request is already "+user_request.status)
            return redirect(url_for('main.user_consumer_request_detail',username=username,request_id=request_id))
    return render_template('admin_user_consumer_requests.html', form=form, form2=form2, username=username,user_request=user_request,consumer_file=consumer_file)

@main.route('/admin/users/<username>/commercial-request', methods=['GET', 'POST'])
@login_required
@admin_required
def user_commercial_request_detail(username):
    '''
    admin can see users commercial requests and upload file against the requests.
    also numbering the file
    '''
    form = UploadConsumerFileForm()
    form2 = ReturnRemarkForm()
    user = User.query.filter_by(username=username).first()
    request_id = request.args.get('request_id')
    user_request = user.commercial_requests.filter_by(id=request_id).first()
    commercial_file = user_request.commercial_report
    if form2.validate_on_submit() and form2.return_req.data:
        if user_request.status=="Pending":
            user_request.status = "Returned"
            user_request.remark = form2.remark.data
            db.session.commit()
        else:
            flash("The request is already "+user_request.status)
        return redirect(url_for('main.user_commercial_request_detail',username=username,request_id=request_id))
    # commercial_file=Commercial_report.query.filter_by(commercial_request_id=request_id).filter_by(user_id=user.id).first()
    if form.validate_on_submit() and form.submit.data or form.reject.data:
        if user_request.status=="Pending":
            if form.submit.data:
                report = request.files['report']
                if report.filename == "":
                    flash('No file is selected.')
                    return redirect(url_for('main.user_commercial_request_detail',username=username,request_id=request_id))
                filename = secure_filename(report.filename)
                if user_request.commercial_report:
                    flash("File is already uploaded..")
                    return redirect(url_for('main.user_commercial_request_detail',username=username,request_id=request_id))
                else:
                    if allowed_file(report.filename):
                        part1 = filename.split('.')
                        today_date_with_slace=str(date.today().strftime('%d-%m-%Y'))
                        today_date_array=today_date_with_slace.split('-')
                        today_date=''
                        for getdate in today_date_array:
                            today_date=today_date+getdate
                        name_with_white_space=user_request.name_of_unit.split(' ')
                        full_name=''
                        for name in name_with_white_space:
                            full_name=full_name+name
                        part1[0]='Commercial_'+full_name+'_'+today_date+'_'+user.username
                        new_filename = part1[0] + '.' + part1[1]
                        commercial_report = Commercial_report(uploaded_file=new_filename, uploaded_time=datetime.now(), commercial_request_id=request_id, user_id=user.id)                
                        db.session.add(commercial_report)
                        db.session.commit()
                        report.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
                        return redirect(url_for('main.user_commercial_request_detail',username=username,request_id=request_id))
                    else:
                        return redirect(url_for('main.user_commercial_request_detail',username=username,request_id=request_id))
            elif form.reject.data:
                user_request.status="Rejected"
                db.session.commit()
                flash("Rejected the request.")
                return redirect(url_for('main.user_commercial_request_detail',username=username,request_id=request_id))
        else:
            flash("The request is already "+user_request.status)
            return redirect(url_for('main.user_commercial_request_detail',username=username,request_id=request_id))
    return render_template('admin_user_commercial_requests.html', form=form,form2=form2, username=username,user_request=user_request,commercial_file=commercial_file)


@main.route('/admin/users/<username>', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_edit_user_profile(username):
    '''
    admin can update the user's profile.
    '''
    form = AdminEditUserProfileForm(username)
    user = User.query.filter_by(username=username).first()
    if form.validate_on_submit():
        if form.role.data == 3:
            return redirect(url_for('main.edit_profile_admin'))
        user.email = form.email.data
        user.username = form.username.data
        user.name = form.name.data
        user.role_id = form.role.data
        user.location = form.location.data
        db.session.add(user)
        db.session.commit()
        flash('User profile has been updated.')
        return redirect(url_for('main.admin_edit_user_profile', username=username))
    form.email.data = user.email
    form.username.data = user.username
    form.name.data = user.name
    form.role.data = user.role_id
    form.location.data = user.location
    page = request.args.get('page', 1, type=int)
    pagination = Consumer_request.query.filter_by(user_id=user.id).order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
    user_consumer_request = pagination.items
    return render_template('admin_edit_user_profile.html', form=form, username=username,user=user,user_consumer_request=user_consumer_request,pagination=pagination)

@main.route('/admin/users/<username>/consumer_requests', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user_consumer_request(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = Consumer_request.query.filter_by(user_id=user.id).order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
    user_consumer_request = pagination.items
    return render_template('admin_user_all_consumer_requests.html', username=username, user=user,user_consumer_request=user_consumer_request,pagination=pagination)


@main.route('/admin/users/<username>/conmmercial_requests', methods=['GET', 'POST'])
@login_required
@admin_required
def admin_user_commercial_request(username):
    user = User.query.filter_by(username=username).first()
    page = request.args.get('page', 1, type=int)
    pagination = Commercial_request.query.filter_by(user_id=user.id).order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
    user_commercial_request = pagination.items
    return render_template('admin_user_all_commercial_requests.html', username=username, user=user,user_commercial_request=user_commercial_request,pagination=pagination)

@main.route('/admin/users/<username>/delete', methods=['GET', 'POST'])
@login_required
@admin_required
def delete_user(username):
    '''
    admin can delete a user
    '''
    form = DeleteUserForm()
    user = User.query.filter_by(username=username).first()
    if form.validate_on_submit():
        yesNo = form.yes_no.data
        if yesNo == "yes":
            db.session.delete(user)
            db.session.commit()
            flash(f'User account has been deleted successfully.')
            return redirect(url_for('main.admin_home'))
        else:
            return redirect(url_for('main.admin_home'))
    return render_template('admin_delete_user.html', username=username, form=form)


@main.route('/admin/profile')
@login_required
@admin_required
def admin_profile():
    '''
    admin profile page
    '''
    admin = User.query.filter_by(username=current_user.username).first()
    return render_template('admin_profile.html', admin=admin)

@main.route('/admin/edit-profile', methods=['GET', 'POST'])
@login_required
@admin_required
def edit_profile_admin():
    '''
    Edit profile of the admin page
    '''
    form = AdminEditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.admin_profile'))
    form.name.data = current_user.name
    form.location.data = current_user.location
    return render_template('edit_profile_admin.html', form=form)

@main.route('/admin/reset-password', methods=["GET", "POST"])
@login_required
@admin_required
def admin_reset_password():
    '''
    Admin can change his password
    '''
    form = AdminResetPasswordForm()
    user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash("Your password has been changed successfully.")
        return redirect(url_for('main.admin_profile'))
    return render_template('admin_reset_password.html', form=form)

# ..............................coding part of report admin.....................................


@main.route('/report-admin')
@login_required
def report_admin_home():
    form = AdminConsumerRequestSearchForm()
    page = request.args.get('page', 1, type=int)
    if request.args.get('search_name') and request.args.get('search_username') and request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('search_name')
        search_value3 = request.args.get('from_date')
        search_value4 = request.args.get('to_date')
        search_value5 = request.args.get('status')
        form.status.data = search_value5
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.request_date.between(search_value3, search_value4)).filter(Consumer_request.status.like('%'+f'{search_value5}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('report_admin_home.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.report_admin_home'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.request_date.between(search_value3, search_value4)).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name') and request.args.get('search_username') and request.args.get('from_date'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('search_name')
        search_value3 = request.args.get('from_date')
        search_value4 = date.today()
        search_value5 = request.args.get('status')
        form.status.data = search_value5
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.request_date.between(search_value3, search_value4)).filter(Consumer_request.status.like('%'+f'{search_value5}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('report_admin_home.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.report_admin_home'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.request_date.between(search_value3, search_value4)).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_username') and request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value4}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('report_admin_home.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.report_admin_home'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.request_date.between(search_value2, search_value3)).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name') and request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('search_name')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        consumer_req = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value4}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name') and request.args.get('search_username'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('search_name')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('report_admin_home.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.report_admin_home'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.name.like('%'+f'{search_value2}'+'%')).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_username') and request.args.get('from_date'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('report_admin_home.html', form=form,consumer_req=consumer_req)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.report_admin_home'))
        # consumer_req = user.consumer_requests.filter(Consumer_request.request_date.between(search_value2, search_value3)).order_by(Consumer_request.request_time.desc())      
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name') and request.args.get('from_date'):
        search_value1 = request.args.get('search_name')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        consumer_req = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.request_date.between(search_value2, search_value3)).filter(Consumer_request.status.like('%'+f'{search_value4}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('from_date') and request.args.get('to_date'):
        search_value1 = request.args.get('from_date')
        search_value2 = request.args.get('to_date')
        search_value3 = request.args.get('status')
        form.status.data=search_value3
        consumer_req = Consumer_request.query.filter(Consumer_request.request_date.between(search_value1, search_value2)).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_username'):
        search_value1 = request.args.get('search_username')
        search_value2 = request.args.get('status')
        form.status.data=search_value2
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            consumer_req = Consumer_request.query.filter_by(user_id=user.id).filter(Consumer_request.status.like('%'+f'{search_value2}'+'%')).order_by(Consumer_request.request_time.desc())
            return render_template('report_admin_home.html', form=form,consumer_requests=consumer_requests)
        else:
            flash('User does not exist.')
            pagination = Consumer_request.query.order_by(Consumer_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            consumer_requests = pagination.items
            return redirect(url_for('main.report_admin_home'))
        # consumer_req = user.consumer_requests.order_by(Consumer_request.request_time.desc())
        # return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('search_name'):
        search_value1 = request.args.get('search_name')
        search_value2 = request.args.get('status')
        form.status.data = search_value2
        consumer_req = Consumer_request.query.filter(Consumer_request.name.like('%'+f'{search_value1}'+'%')).filter(Consumer_request.status.like('%'+f'{search_value2}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('from_date'):
        search_value1 = request.args.get('from_date')
        search_value2 = date.today()
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        consumer_req = Consumer_request.query.filter(Consumer_request.request_date.between(search_value1, search_value2)).filter(Consumer_request.status.like('%'+f'{search_value3}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    elif request.args.get('status'):
        search_value1 = request.args.get('status')
        form.status.data = search_value1
        consumer_req = Consumer_request.query.filter(Consumer_request.status.like('%'+f'{search_value1}'+'%')).order_by(Consumer_request.request_time.desc())      
        return render_template('report_admin_home.html', consumer_req=consumer_req, form=form)
    else:
        pagination = Consumer_request.query.filter_by(status="Pending").order_by(Consumer_request.request_time.desc()).paginate(page, per_page=100, error_out=False)
        consumer_requests = pagination.items
    return render_template('report_admin_home.html', form=form,page=page,pagination=pagination,consumer_requests=consumer_requests)

@main.route('/report-admin/commercial-requests')
@login_required
def report_admin_commercial_requests():
    form=AdminCommercialRequestSearchForm()
    page = request.args.get('page', 1, type=int)
    if request.args.get('username') and request.args.get('unit_name') and request.args.get('pan_no') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('pan_no')
        search_value4 = request.args.get('from_date')
        search_value5 = request.args.get('to_date')
        search_value6 = request.args.get('status') 
        form.status.data = search_value6
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.request_date.between(search_value4,search_value5)).filter(Commercial_request.status.like('%'+f'{search_value6}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.request_date.between(search_value4,search_value5)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('unit_name') and request.args.get('pan_no') and request.args.get('from_date') :
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('pan_no')
        search_value4 = request.args.get('from_date')
        search_value5 = date.today()
        search_value6 = request.args.get('status')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.request_date.between(search_value4,search_value5)).filter(Commercial_request.status.like('%'+f'{search_value6}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.request_date.between(search_value4,search_value5)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('unit_name') and request.args.get('pan_no'):
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('pan_no')
        search_value4 = request.args.get('status')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value6}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('unit_name') and request.args.get('from_date') :
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('from_date')
        search_value4 = date.today()
        search_value5 = request.args.get('status')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.request_date.between(search_value3,search_value4)).filter(Commercial_request.status.like('%'+f'{search_value5}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.request_date.between(search_value3,search_value4)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.request_date.between(search_value2,search_value3)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('unit_name') and request.args.get('pan_no') and request.args.get('from_date'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('from_date')
        search_value4 = date.today()
        search_value5 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.request_date.between(search_value3,search_value4)).filter(Commercial_request.status.like('%'+f'{search_value5}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('unit_name') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('pan_no') and request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('pan_no')
        search_value2 = request.args.get('from_date')
        search_value3 = request.args.get('to_date')
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        commercial_requests = user.commercial_requests.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('unit_name'):
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('unit_name')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.name_of_unit.like('%'+f'{search_value2}'+'%')).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('pan_no'):
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') and request.args.get('from_date'):
        search_value1 = request.args.get('username')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.filter(Commercial_request.request_date.between(search_value2,search_value3)).order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('unit_name') and request.args.get('pan_no') :
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('pan_no')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.pan_no.like('%'+f'{search_value2}'+'%')).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('unit_name') and request.args.get('from_date'):
        search_value1 = request.args.get('unit_name')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('pan_no') and request.args.get('from_date'):
        search_value1 = request.args.get('pan_no')
        search_value2 = request.args.get('from_date')
        search_value3 = date.today()
        search_value4 = request.args.get('status')
        form.status.data = search_value4
        commercial_requests = user.commercial_requests.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).filter(Commercial_request.request_date.between(search_value2,search_value3)).filter(Commercial_request.status.like('%'+f'{search_value4}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('from_date') and request.args.get('to_date') :
        search_value1 = request.args.get('from_date')
        search_value2 = request.args.get('to_date')
        search_value3 = request.args.get('status')
        form.status.data = search_value3
        commercial_requests = Commercial_request.query.filter(Commercial_request.request_date.between(search_value1,search_value2)).filter(Commercial_request.status.like('%'+f'{search_value3}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('username') :
        search_value1 = request.args.get('username')
        user = User.query.filter(User.username.like('%'+f'{search_value1}'+'%')).first()
        if user:
            commercial_requests = Commercial_request.query.filter_by(user_id=user.id).order_by(Commercial_request.request_time.desc())
            return render_template('report_admin_commercial_requests.html', commercial_requests=commercial_requests, form=form)
        else:
            flash("User does not exist.")
            pagination = Commercial_request.query.order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
            commercial_req = pagination.items
            return redirect(url_for('main.report_admin_commercial_requests'))
        # commercial_requests = user.commercial_requests.order_by(Commercial_request.request_time.desc())
        # return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('unit_name'):
        search_value1 = request.args.get('unit_name')
        commercial_requests = Commercial_request.query.filter(Commercial_request.name_of_unit.like('%'+f'{search_value1}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('pan_no') :
        search_value1 = request.args.get('pan_no')
        commercial_requests = Commercial_request.query.filter(Commercial_request.pan_no.like('%'+f'{search_value1}'+'%')).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('from_date'):
        search_value1 = request.args.get('from_date')
        search_value2 = date.today()
        commercial_requests = Commercial_request.query.filter(Commercial_request.request_date.between(search_value1,search_value2)).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', form=form, commercial_requests=commercial_requests,page=page)
    elif request.args.get('status'):
        search_value1=request.args.get('status')
        form.status.data=search_value1
        commercial_requests = Commercial_request.query.filter_by(status=search_value1).order_by(Commercial_request.request_time.desc())
        return render_template('report_admin_commercial_requests.html', commercial_requests=commercial_requests, form=form)
    pagination = Commercial_request.query.filter_by(status="Pending").order_by(Commercial_request.request_time.desc()).paginate(page, per_page=current_app.config['CONSUMER_REQ_PER_PAGE'], error_out=False)
    commercial_req = pagination.items
    return render_template('report_admin_commercial_requests.html', commercial_req=commercial_req, form=form,pagination=pagination,page=page)


@main.route('/report-admin/profile/<username>')
@login_required
def report_admin_profile(username):
    '''
    showing report-admin profile
    '''
    user = User.query.filter_by(username=username).first_or_404()
    return render_template('report_admin_profile.html', user=user)

@main.route('/report-admin/edit-profile/<username>', methods=['GET', 'POST'])
@login_required
def report_admin_edit_profile(username):
    '''
    Update report-admin profile
    '''
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.name = form.name.data
        current_user.location = form.location.data
        db.session.add(current_user._get_current_object())
        db.session.commit()
        flash('Your profile has been updated.')
        return redirect(url_for('.report_admin_profile', username=current_user.username))
    form.name.data = current_user.name
    form.location.data = current_user.location
    return render_template('report_admin_edit_profile.html', form=form)

@main.route('/report-admin/<username>/consumer-request/', methods=['GET', 'POST'])
@login_required
def report_admin_consumer_request_detail(username):
    form = UploadConsumerFileForm()
    form2=ReturnRemarkForm()
    request_id = request.args.get('request_id')
    user = User.query.filter_by(username=username).first()
    user_request = user.consumer_requests.filter_by(id=request_id).first()
    # consumer_file=Consumer_report.query.filter_by(consumer_request_id=request_id).filter_by(user_id=user.id).first()
    consumer_file = user_request.consumer_report    # to get the uploaded consumer file
    if form2.validate_on_submit() and form2.return_req.data:
        if user_request.status=="Pending":
            user_request.status = "Returned"
            user_request.remark = form2.remark.data
            db.session.commit()
        else:
            flash("The request is already "+user_request.status)
        return redirect(url_for('main.report_admin_consumer_request_detail',username=username,request_id=request_id))
    if form.validate_on_submit() and form.submit.data or form.reject.data:
        if user_request.status=="Pending":
            if form.submit.data:
                report = request.files['report']
                if report.filename == "":
                    flash('No file is selected.')
                    return redirect(url_for('main.report_admin_consumer_request_detail', username=username, request_id=user_request.id))
                filename = secure_filename(report.filename)
                if user_request.consumer_report:
                    flash("File is already uploaded..")
                    return redirect(url_for('main.report_admin_consumer_request_detail', username=username, request_id=user_request.id))
                else:
                    if allowed_file(report.filename):
                        part1 = filename.split('.')
                        today_date_with_slace=str(date.today().strftime('%d-%m-%Y'))
                        today_date_array=today_date_with_slace.split('-')
                        today_date=''
                        for getdate in today_date_array:
                            today_date=today_date+getdate
                        name_with_white_space=user_request.name.split(' ')
                        full_name=''
                        for name in name_with_white_space:
                            full_name=full_name+name
                        part1[0]=full_name+'_consumer_'+today_date
                        new_filename = part1[0] + '.' + part1[1]
                        consumer_report = Consumer_report(uploaded_file=new_filename, uploaded_time=datetime.now(), consumer_request_id=request_id, user_id=user.id)                
                        db.session.add(consumer_report)
                        user_request.status="Completed"
                        db.session.commit()
                        report.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
                    return redirect(url_for('main.report_admin_consumer_request_detail', username=username, request_id=user_request.id))
            elif form.reject.data:
                user_request.status="Rejected"
                db.session.commit()
                flash("Rejected the request.")
                return redirect(url_for('main.report_admin_consumer_request_detail',username=username,request_id=request_id))
        else:
            flash("The request is already "+user_request.status)
            return redirect(url_for('main.report_admin_consumer_request_detail',username=username,request_id=request_id))
    return render_template('report_admin_user_consumer_requests.html', form=form, form2=form2, username=username,user_request=user_request,consumer_file=consumer_file)

@main.route('/report-admin/<username>/commercial-request', methods=['GET', 'POST'])
@login_required
def report_admin_commercial_request_detail(username):
    '''
    report-admin can see users commercial requests and upload file against the requests.
    also numbering the file
    '''
    form = UploadConsumerFileForm()
    form2=ReturnRemarkForm()
    user = User.query.filter_by(username=username).first()
    request_id = request.args.get('request_id')
    user_request = user.commercial_requests.filter_by(id=request_id).first()
    commercial_file = user_request.commercial_report
    # commercial_file=Commercial_report.query.filter_by(commercial_request_id=request_id).first()
    if form2.validate_on_submit() and form2.return_req.data:
        if user_request.status=="Pending":
            user_request.status = "Returned"
            user_request.remark = form2.remark.data
            db.session.commit()
        else:
            flash("The request is already "+user_request.status)
        return redirect(url_for('main.report_admin_commercial_request_detail',username=username,request_id=request_id))
    if form.validate_on_submit() and form.submit.data or form.reject.data:
        if user_request.status=="Pending":
            if form.submit.data:
                report = request.files['report']
                if report.filename == "":
                    flash('No file is selected.')
                    return redirect(url_for('main.report_admin_commercial_request_detail', username=username, request_id=user_request.id, user_request=user_request,commercial_file=commercial_file))
                filename = secure_filename(report.filename)
                if user_request.commercial_report:
                    flash("File is already uploaded..")
                    return redirect(url_for('main.report_admin_commercial_request_detail', username=username, request_id=user_request.id, user_request=user_request,commercial_file=commercial_file))
                else:
                    if allowed_file(report.filename):
                        part1 = filename.split('.')
                        today_date_with_slace=str(date.today().strftime('%d-%m-%Y'))
                        today_date_array=today_date_with_slace.split('-')
                        today_date=''
                        for getdate in today_date_array:
                            today_date=today_date+getdate
                        name_with_white_space=user_request.name_of_unit.split(' ')
                        full_name=''
                        for name in name_with_white_space:
                            full_name=full_name+name
                        part1[0]='Commercial_'+full_name+'_'+today_date+'_'+user.username
                        new_filename = part1[0] + '.' + part1[1]
                        commercial_report = Commercial_report(uploaded_file=new_filename, uploaded_time=datetime.now(), commercial_request_id=request_id, user_id=user.id)                
                        db.session.add(commercial_report)
                        user_request.status="Completed"
                        db.session.commit()
                        report.save(os.path.join(current_app.config['UPLOAD_FOLDER'], new_filename))
                        return redirect(url_for('main.report_admin_commercial_request_detail', username=username, request_id=user_request.id, user_request=user_request,commercial_file=commercial_file))
                    else:
                        return redirect(url_for('main.user_commercial_request_detail', username=username, request_id=user_request.id, user_request=user_request,commercial_file=commercial_file))
            elif form.reject.data:
                user_request.status="Rejected"
                db.session.commit()
                flash("Rejected the request.")
                return redirect(url_for('main.report_admin_commercial_request_detail',username=username,request_id=request_id))
        else:
            flash("The request is already "+user_request.status)
            return redirect(url_for('main.report_admin_commercial_request_detail',username=username,request_id=request_id))
    return render_template('report_admin_user_commercial_requests.html', form=form, form2=form2, username=username,user_request=user_request,commercial_file=commercial_file)

@main.route('/report-admin/reset-password', methods=["GET", "POST"])
def report_admin_reset_password():
    '''
    report-admin can change his password
    '''
    form = AdminResetPasswordForm()
    user = User.query.filter_by(username=current_user.username).first()
    if form.validate_on_submit():
        user.password = form.password.data
        db.session.commit()
        flash("Your password is changed successfully.")
        return redirect(url_for('main.report_admin_profile', username=user.username))
    return render_template('report_admin_reset_password.html', form=form)

# ..............................pdf generation code for user......................................


@main.route('/consumer-request-pdf')
def pdf_consumer_request():
    '''
    Code for generating consumer request pdf for user
    '''
    request_id = request.args.get('request_id')
    user = User.query.filter_by(username=current_user.username).first()
    consumer_request = user.consumer_requests.filter_by(id=request_id).first()
    rendered = render_template('pdf_consumer_request.html', consumer_request=consumer_request, user=user)
    css = "app/static/styles/pdf_styling.css"
    pdf = pdfkit.from_string(rendered, False,css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Disposition'] = "inline;filename=Consumer-request.pdf"

    return response


@main.route('/commercial-request-pdf')
def pdf_commercial_request():
    '''
    Code for generating commercial request pdf for user
    '''
    request_id = request.args.get('request_id')
    user = User.query.filter_by(username=current_user.username).first()
    commercial_request = user.commercial_requests.filter_by(
        id=request_id).first()
    rendered = render_template('pdf_commercial_request.html', commercial_request=commercial_request, user=user)
    css = "app/static/styles/pdf_styling.css"
    pdf = pdfkit.from_string(rendered, False,css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Disposition'] = "inline;filename=Commercial-request.pdf"

    return response


@main.route('/admin/consumer-request-pdf')
def admin_pdf_consumer_request():
    '''
    Code for generating consumer request pdf for admin
    '''
    username = request.args.get('username')
    request_id = request.args.get('request_id')
    user = User.query.filter_by(username=username).first()
    consumer_request = user.consumer_requests.filter_by(id=request_id).first()
    rendered = render_template('pdf_consumer_request.html', consumer_request=consumer_request, user=user)
    css = "app/static/styles/pdf_styling.css"
    pdf = pdfkit.from_string(rendered, False,css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Disposition'] = "inline;filename=Consumer-request.pdf"

    return response


@main.route('/admin/commercial-request-pdf')
def admin_pdf_commercial_request():
    '''
    Code for generating commercial request pdf for admin
    '''
    username = request.args.get('username')
    request_id = request.args.get('request_id')
    user = User.query.filter_by(username=username).first()
    commercial_request = user.commercial_requests.filter_by(
        id=request_id).first()
    rendered = render_template('pdf_commercial_request.html', commercial_request=commercial_request, user=user)
    css = "app/static/styles/pdf_styling.css"
    pdf = pdfkit.from_string(rendered, False,css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Disposition'] = "inline;filename=Commercial-request.pdf"

    return response


@main.route('/report-admin/consumer-request-pdf')
def report_admin_pdf_consumer_request():
    '''
    Code for generating consumer request pdf for report-admin
    '''
    username = request.args.get('username')
    request_id = request.args.get('request_id')
    user = User.query.filter_by(username=username).first()
    consumer_request = user.consumer_requests.filter_by(id=request_id).first()
    rendered = render_template('pdf_consumer_request.html', consumer_request=consumer_request, user=user)
    css = "app/static/styles/pdf_styling.css"
    pdf = pdfkit.from_string(rendered, False,css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Disposition'] = "inline;filename=Consumer-request.pdf"

    return response


@main.route('/report-admin/commercial-request-pdf')
def report_admin_pdf_commercial_request():
    '''
    Code for generating commercial request pdf for report-admin
    '''
    username = request.args.get('username')
    request_id = request.args.get('request_id')
    user = User.query.filter_by(username=username).first()
    commercial_request = user.commercial_requests.filter_by(
        id=request_id).first()
    rendered = render_template('pdf_commercial_request.html', commercial_request=commercial_request, user=user)
    css = "app/static/styles/pdf_styling.css"
    pdf = pdfkit.from_string(rendered, False,css=css)

    response = make_response(pdf)
    response.headers['Content-Type'] = "application/pdf"
    response.headers['Content-Disposition'] = "inline;filename=Commercial-request.pdf"

    return response
