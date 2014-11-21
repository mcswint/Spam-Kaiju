import imaplib
import email
import mailbox
import sys
import csv
import time
import datetime

sys.path.append('dbsetup')
from setup_db_SA import Email, Base, Brand
from parseBody import parseBody
from parse_image_links import parse_links
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

engine = create_engine('sqlite:///emails2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()


def stringToDateTimeObject(date_string):
    if (date_string[24] == " "): # Fri, 8 Aug 2014 12:33:52 -0000
        date_time_object = time.strptime(date_string[5:24], '%d %b %Y %X')
    elif (date_string[0].isdigit()):  # 8 Aug 2014 12:33:52 -0000
        date_time_object = time.strptime(date_string[:19], '%d %b %Y %X')
    else: # Fri, 22 Aug 2014 12:33:52 -0000
        date_time_object = time.strptime(date_string[5:25], '%d %b %Y %X')
