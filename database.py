
import logging
logging.basicConfig(level=logging.CRITICAL, force=True)
logging.getLogger('sqlalchemy.engine').setLevel(logging.CRITICAL)
logging.getLogger('sqlalchemy.engine').handlers.clear()


import datetime
from inspect import CO_ASYNC_GENERATOR
from sqlalchemy import TIMESTAMP, PrimaryKeyConstraint, create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, Float, DateTime, Date
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref


engine = create_engine("sqlite:///:memory:", echo=False)
base = declarative_base()
connection = engine.connect()

class Lead(base):

    __tablename__ = 'leads'

    address = Column(String(255))
    city = Column(String(255))
    club_id = Column(Integer, ForeignKey('club.club_id'))
    staff_id = Column(Integer, ForeignKey('staff.staff_id'))
    country = Column(String(255)) 
    creation_date = Column(Date)
    conversion_date = Column(Date)
    date_of_birth = Column(Date)
    first_name = Column(String(255))
    gender = Column(String(255))
    last_name = Column(String(255))
    lead_id = Column(Integer, primary_key = True)
    notes = Column(String(255))
    preffered_contact_method = Column(String(255))
    status = Column(String(255))
    
    
class Club(base):

    __tablename__ = 'club'
    club_id = Column(Integer, primary_key = True)
    preffered_contact_method = Column(String(255))
    status = Column(String(255))
    city = Column(String(255))
    country = Column(String(255))

   

class Staff(base):

    __tablename__ = 'staff'
    staff_id = Column(Integer, primary_key = True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    preffered_contact_method = Column(String(255))
    club_id = Column(Integer, ForeignKey('club.club_id'))
    dept_name = Column(String(255))
    working_status = Column(String(255))
    rating = Column(Float)


class Member(base):
    __tablename__ = 'member'
    member_id = Column(Integer, primary_key = True)
    first_name = Column(String(255))
    last_name = Column(String(255))
    date_of_birth = Column(Date)
    gender = Column(String(255))

class Subscription(base):
    __tablename__ = 'subscription'
    sub_id = Column(Integer, primary_key = True)
    conversation_date = Column(String(255), ForeignKey('leads.conversion_date'))
    member_id = Column(Integer, ForeignKey('member.member_id'))
    end_date = Column(Date)
    status = Column(String(255))
    type = Column(String(255))
    amount = Column(Float)
    

base.metadata.create_all(engine)

