import imaplib
import email
import mailbox
import sys
import csv
import json


sys.path.append('dbsetup')
from setup_db_SA import Email, Base, Brand, Email_Address
from parse_image_links import parse_links
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

engine = create_engine('sqlite:///emails2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

class tranformer():
    
    def matchBrandsToEmails(self):
        print("start")
        brands = session.query(Brand)
        #print(type(brands))
        tupDict = {}

        for brand in brands:
            brandId = brand.id
            addresses = []
            emails = []

            for currentEmailAddress in session.query(Email_Address.id).filter(Email_Address.brand_id == brandId):
                addresses.append(currentEmailAddress)

            for address in addresses:
                for entry in session.query(Email).filter(Email.address_id == address.id):
                    emails.append(entry)
            
            addressToEmailTuple = (addresses, emails)
            tupDict[brand] = addressToEmailTuple

        # a Dictionary of brands ("brand name" :(list of addressess associated with brand, all emails from all addresses associated with brand)) 
        return tupDict;

    def countEmailsbyBrand(self, tupDict):
        emailString = ""
        topDict = {}
        categoryDict = {}
        brandDict = {}

        for key, val in tupDict.items():
            numEmails = len(val[1])
            if numEmails != 0:
                brandDict[key.brand_name] = numEmails
        
        topDict["name"] = brandDict
        print(brandDict)
        input("Enter...")

        emailString += json.dumps(topDict, indent=4, separators=(',', ': '))
        print(emailString)
        #print (key.brand_name)
        #print ("num of emails: ", numEmails)
        #jsonString = json.dumps({'name': 'flare', 'children': [emailString]}, indent=4,
        #                separators=(',', ': '))
        #print(jsonString)

def writeToCsv():
    #with csv.writer(open('test.csv', 'w', newLine='') as datafile:
    pass


def main():
    t = tranformer()
    brandDict = t.matchBrandsToEmails()
    t.countEmailsbyBrand(brandDict)

    #t.writeToCsv

if __name__ =='__main__':
    main()
