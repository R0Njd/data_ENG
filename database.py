from audioop import add
import datetime
from inspect import CO_ASYNC_GENERATOR
from sqlalchemy import TIMESTAMP, PrimaryKeyConstraint, create_engine
from sqlalchemy import Column, String, Integer, Boolean, ForeignKey, Table, Float, DateTime, Date
import sqlalchemy
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm import relationship, backref


engine = create_engine("sqlite:///:memory:", echo=True)
base = declarative_base()
connection = engine.connect()

class Lead(base):

    __tablename__ = 'leads'

    address = Column(String(255))
    city = Column(String(255))
    club_id = Column(Integer, ForeignKey('club.club_id'))
    conversion_date = Column(Date)
    country = Column(String(255)) 
    creation_date = Column(Date)
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
    
base.metadata.create_all(engine)
   

