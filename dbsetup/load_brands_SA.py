from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import csv
import sys

from setup_db_SA import Base, Brand

engine = create_engine('sqlite:///../emails2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

with open('brands_and_websites.csv') as datafile:
	data = csv.reader(datafile, delimiter=',')
	for row in data:
		website = row[1]
		cleanWeb = ""
		count = website.count(".")
		pieces = website.split(".")
		if (count == 0):
			print (website)
			continue
		if (count == 1):
			#print(pieces[0])
			cleanWeb = pieces[0]
		else:
			#print(pieces[1])	
			cleanWeb = pieces[1]

		new_brand = Brand(brand_name=row[0], brand_website=website, brand_website_clean = cleanWeb)	
		session.add(new_brand)
	session.commit()

# for testing
#brand = session.query(Brand)
#for b in brand:
#	print(b.id, b.brand_name, b.brand_website)
