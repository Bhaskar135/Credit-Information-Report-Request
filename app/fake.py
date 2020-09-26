from random import randint
from sqlalchemy.exc import IntegrityError
from faker import Faker
from .import db
from .models import User,Consumer_request,Commercial_request

def users(count=100):
    fake = Faker()
    i=0
    while i<count:
        u=User(email=fake.email(), username=fake.user_name(), password='password', name=fake.name() )
        db.session.add(u)
        try:
            db.session.commit()
            i+=1
        except IntegrityError:
            db.session.rollback()

def consumer_requests(count=100):
    fake=Faker()
    user_count=User.query.count()
    for i in range(count):
        u=User.query.offset(randint(0,user_count-1)).first()
        request=Consumer_request(
            name=fake.name(),
            gender='male',
            dob=fake.date(),
            loan_amount=fake.random_int(6),
            pan_no=fake.random_int(10),
            aadhaar_no=fake.random_int(10),
            voter_id=fake.random_int(10),
            passport=fake.random_int(10),
            driving_license_no=fake.random_int(10),
            address=fake.city(),
            state=fake.state(),
            pin_code=fake.random_int(6),
            request_time=fake.date(),
            user=u
        )
        db.session.add(request)
    db.session.commit()

def commercial_requests(count=100):
    fake=Faker()
    user_count=User.query.count()
    for i in range(count):
        u=User.query.offset(randint(0,user_count-1)).first()
        request=Commercial_request(
            name_of_unit=fake.word(),
            pan_no=fake.random_int(10),
            entity_type=fake.word(),
            class_of_activity=fake.word(),
            date_of_reg=fake.date(),
            address=fake.address(),
            pin_code=fake.random_int(6),
            state=fake.state(),
            city=fake.city(),
            enquiry_type=fake.word(),
            loan_amount=fake.random_int(6),
            request_time=fake.date(),
            user=u
        )
        db.session.add(request)
    db.session.commit()






