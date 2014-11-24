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
        brands = session.query(Brand)
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

    def emailsSocial(self, tupDict):

        allCat = {}
   
        for key, val in tupDict.items():
            if len(val[1]) > 0:
     
                if key.category in allCat:
                    tempList = allCat[key.category]
                    allCat[key.category] = tempList + val[1]
                else:
                    allCat[key.category] = val[1]

        onelist = ["category"]
        social = {"facebook" : [], "twitter":[], "pinterest":[], "youtube":[], "instagram":[]}
        for key, val in allCat.items():
            onelist.append(key)
            totalEmails = 0
            facebook = 0
            twitter = 0
            pinterest = 0
            youtube = 0
            instagram = 0
            for v in val:
                totalEmails += 1
                socailLinks = v.social_links.split(",")
                for link in socailLinks:
                    if "facebook" in link:
                        facebook += 1
                    elif "twitter" in link:
                        twitter += 1
                    elif "pinterest" in link:
                        pinterest += 1
                    elif "youtube" in link:
                        youtube += 1
                    elif "instagram" in link:
                        instagram +=1
            social["facebook"].append((key, (facebook/totalEmails)*100))
            social["twitter"].append((key, (twitter/totalEmails)*100)) 
            social["pinterest"].append((key, (pinterest/totalEmails)*100)) 
            social["youtube"].append((key, (youtube/totalEmails)*100)) 
            social["instagram"].append((key, (instagram/totalEmails)*100))        

        
        data = [onelist]
        for metric, val in social.items():
            tempList = [metric]
            for count in val:
                tempList.append(count[1])
            data.append(tempList)

        with open('socialData.csv', 'w', newline='') as fp:
            a = csv.writer(fp, delimiter=',')
            a.writerows(data)
        print (data) 


    def countEmailsbyBrand(self, tupDict):
        emailString = ""

        topDict = {}
        allCategories = []

        # build category dictionaries from brands
        for key, val in tupDict.items():
            numEmails = len(val[1])
            if numEmails != 0:
                
                brandDict = {} 
                brandDict["name"] = key.brand_name
                brandDict["size"] = numEmails

                found = False

                # check allCategories for key.category
                for category in allCategories:
                    if category["name"] == key.category:
                        found = True
                        associatedBrands = category["children"]
                        associatedBrands.append(brandDict)
                        category["children"] = associatedBrands

                # add key.category to allCategories
                if not found:
                    categoryDict = {}
                    categoryDict["name"] = key.category # build a new categoryDict
                    categoryDict["children"] = [brandDict]
                    allCategories.append(categoryDict)
                
        topDict["name"] = "flare"
        topDict["children"] = allCategories

        emailString += json.dumps(topDict, indent=4, separators=(',', ': '))
        print(emailString)


def main():
    t = tranformer()
    brandDict = t.matchBrandsToEmails()
    t.countEmailsbyBrand(brandDict)
    t.emailsSocial(brandDict)

if __name__ =='__main__':
    main()
