import imaplib
import email
import mailbox
import sys
import csv
import json
import time
import datetime

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


def stringToDateTimeObject(date_string):
   
    if (date_string[24] == " "): # Fri, 8 Aug 2014 12:33:52 -0000
        date_time_object = time.strptime(date_string[5:24], '%d %b %Y %X')
    elif (date_string[0].isdigit()):  # 8 Aug 2014 12:33:52 -0000
        date_time_object = time.strptime(date_string[:19], '%d %b %Y %X')
    else: # Fri, 22 Aug 2014 12:33:52 -0000
        date_time_object = time.strptime(date_string[5:25], '%d %b %Y %X')
    return date_time_object
    
class timeTransformer():

    def getAllEmailDatesInRange(self, start_time, end_time):
       allEmails = session.query(Email)
       emailsInRange = []
       for email in allEmails:
           dateTimeObject = stringToDateTimeObject(email.time_sent)

           if dateTimeObject > start_time and dateTimeObject < end_time:
               emailsInRange.append(email)
       return emailsInRange


    def matchBrandsToEmails(self, cleanEmails):
        brands = session.query(Brand)
        tupDict = {}

        for brand in brands:
            brandId = brand.id
            associatedEmails = []
            
            for currentEmailAddress in session.query(Email_Address).filter(Email_Address.brand_id == brandId):
                associatedEmails.append(currentEmailAddress.email_address)
                
            for email in cleanEmails:
                if email in associatedEmails:
                    brandName = brand.brand_name
                    if brandName in tupDict:
                        numberOfEmails = tupDict[brandName]
                        numberOfEmails = numberOfEmails + 1
                        tupDict[brandName] = numberOfEmails
                    else:
                        tupDict[brandName] = 1
        return tupDict
        # a Dictionary of brands ("brand name" :(list of addressess associated with brand, all emails from all addresses associated with brand)) 


    def buildJSON(self, tupDict):
        emailString = ""

        topDict = {}
        allBrands = []

        # build category dictionaries from brands
        for key, value in tupDict.items():
            brandDict = {} 
            brandDict["name"] = key
            brandDict["size"] = value
            allBrands.append(brandDict)
                
        topDict["name"] = "flare"
        topDict["children"] = allBrands

        emailString += json.dumps(topDict, indent=4, separators=(',', ': '))
        print(emailString)


def main():

    startTime = input("Please enter a start time (Format : 31 Dec 2013 21:30:00)\n")
    start_time_object = time.strptime(startTime, '%d %b %Y %X')

    endTime = input("Please enter an end time (Format : 31 Dec 2013 21:30:00)\n")
    end_time_object = time.strptime(endTime, '%d %b %Y %X')

    t = timeTransformer()
    emailsInRange = t.getAllEmailDatesInRange(start_time_object, end_time_object)
    cleanEmails = []
    for email in emailsInRange:
        cleanEmails.append(email.sender_address)

    brandToNumberDictionary = t.matchBrandsToEmails(cleanEmails)
    
    t.buildJSON(brandToNumberDictionary)


if __name__ =='__main__':
    main()