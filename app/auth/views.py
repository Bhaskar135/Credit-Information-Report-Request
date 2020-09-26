from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, logout_user, login_required,current_user
from . import auth
from ..models import User,Role
from .. import db
from .forms import LoginForm, RegistrationForm, ForgotPasswordForm, ResetForgotPasswordForm
from ..email import send_email

@auth.route('/login',methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user=User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user,form.remember_me.data)
            next=request.args.get('next')
            if next is None or not next.startswith('/'):
                next=url_for('main.home')
            return redirect(next)
        flash('Invalid username or password.')
    return render_template('auth/login.html',form=form)

@auth.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('main.home'))

@auth.route('/register',methods=['GET','POST'])
def register():
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
            flash('You can now login.')
            return redirect(url_for('auth.login'))
    return render_template('auth/register.html',form=form)

@auth.route('/forgot-password',methods=['GET','POST'])
def forgot_password_link_send():
    form=ForgotPasswordForm()
    if form.validate_on_submit():
        email=form.email.data
        user=User.query.filter_by(email=email).first()
        if user:
            token=user.generate_forgot_password_token()
            send_email(user.email,'auth/email/forgot_password', user=user,token=token)
            return redirect(url_for('auth.login'))
        else:
            return redirect(url_for('auth.forgot_password_link_send'))
    return render_template('auth/forgot_password.html',form=form)

@auth.route('/reset_password',methods=["GET","POST"])
def reset_password():
    form=ResetForgotPasswordForm()
    user_id=request.args.get('user_id')
    user=User.query.filter_by(id=user_id).first()
    if form.validate_on_submit():
        user.password=form.password.data
        db.session.commit()
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html',form=form)














