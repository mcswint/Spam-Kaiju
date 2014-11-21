import imaplib
import email
import mailbox
import sys
import csv

sys.path.append('dbsetup')
from setup_db_SA import Email, Base, Brand, Email_Address
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
    
    def matchBrandsToEmails(self):
        print("start")
        brands = session.query(Brand.id)
        print(type(brands))

        brandsToEmails = []
        for brand in brands:
            brand = brand[0]
            addresses = []
            emails = []

            for currentEmailAddress in session.query(Email_Address.id).filter(Email_Address.brand_id == brand):
                addresses.append(currentEmailAddress[0])
                #input("Enter....")

            for address in addresses:
                for entry in session.query(Email).filter(Email.address_id == address):
                    emails.append(entry)
            
            addressToEmailTuple = (addresses, emails)
            brandsToEmails.append((brand, addressToEmailTuple))

        # a list of tuples ("brand id", (list of addressess associated with brand, all emails from all addresses associated with brand)) 
        print("hello")
        print (brandsToEmails)
        return brandsToEmails

        def countEmailsbyBrand(self):
            pass
     
def main():
    t = tranformer()
    t.matchBrandsToEmails()

if __name__ =='__main__':
    main()