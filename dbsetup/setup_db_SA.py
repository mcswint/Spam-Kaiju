import os
import sys
from sqlalchemy import Column, ForeignKey, Integer, String, Text, DateTime, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine
 
Base = declarative_base()
 
class Brand(Base):
    __tablename__ = 'brand'
    # Here we define columns for the table person
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    brand_name = Column(String(250), nullable=False)
    brand_website = Column(String(250))
    brand_website_clean = Column(String(250))
 

#brand references foreign key, but has to be null so cant be foreign...
class Email_Address(Base):
	__tablename__ = 'email_address'
	id = Column(Integer, primary_key=True)
	email_address = Column(String(250), nullable = False)
	brand = Columnn(Integer)

#not using
class Brand_To_Email_Address(Base):
    __tablename__ = 'brand_to_email_address'
    # Here we define columns for the table address.
    # Notice that each column is also a normal Python instance attribute.
    id = Column(Integer, primary_key=True)
    brand_id = Column(Integer, ForeignKey('brand.id'))
    address_id = Column(Integer, ForeignKey('email_address.id'))

class Email(Base):
	__tablename__ = 'email'

	id = Column(Integer, primary_key=True)
	address_id = Column(Integer, ForeignKey('email_address.id'))
	sender_address = Column(String(250))
	to_address = Column(String(250))
	gmail_label = Column(String(250))
	time_sent = Column(String(250))
	message_id = Column(String(250))
	email_size = Column(String(250))
	subject_line = Column(String(250))
	body_text = Column(Text)
	body_plain = Column(Text)
	body_links = Column(Text)
	body_images = Column(Text)

class Email_Fact_By_Brand(Base):
	__tablename__ = 'email_fact_by_brand'
	id = Column(Integer, primary_key=True)

	brand_id = Column(Integer, ForeignKey('brand.id'))
	fact_date = Column(DateTime)
	email_frequency= Column(Float)
	most_common_word_in_sub= Column(Text)
	per_contain_social_links = Column(Float)
	sent_bday_email = Column(String(100))


 
# Create an engine that stores data in the local directory's
# sqlalchemy_example.db file.
engine = create_engine('sqlite:///../emails2.db')
 
# Create all tables in the engine. This is equivalent to "Create Table"
# statements in raw SQL.
Base.metadata.create_all(engine)