import imaplib
import email
import mailbox
import sys
import csv

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

brands_dict = {}
unmatched = []


class tranformer():
    
    def matchBrandsToEmails():

        brands = session.query(Brand.id)
        print(type(brands))

        brandsToEmails = []
        for brand in brands:
            
            addresses = []
            emails = []

            for currentEmailAddress in session.query(Email_Address).filter_by(brand_id = 'brand'):
                addresses.append(currentEmailAddress)
                input("Enter....")

            for address in emailAddresses:
                for entry in session.query(Email).filter_by(sender_address = 'address')
                    emails.append(entry)
            
            addressToEmailTuple = (addresses, emails)
            brandsToEmails.append(brand, addressToEmailTuple)

        # a list of tuples ("brand id", (list of addressess associated with brand, all emails from all addresses associated with brand)) 
        return brandsToEmails
     
