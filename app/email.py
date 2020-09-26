from flask import current_app, copy_current_request_context, render_template
from .import mail
from threading import Thread
from flask_mail import Message

def send_email(to,template,**kwargs):
    msg=Message(current_app.config['CIRR_MAIL_SUBJECT_PREFIX'], sender=current_app.config['CIRR_MAIL_SENDER'], recipients=[to])
    msg.body=render_template(template+'.txt',**kwargs)
    thr=Thread(target=copy_current_request_context(send_async_email),args=[current_app._get_current_object(),msg])
    thr.start()
    return thr

def send_async_email(app,msg):
    with app.app_context():
        mail.send(msg)