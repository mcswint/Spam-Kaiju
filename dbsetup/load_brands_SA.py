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
		cleanWeb = None
		count = website.count(".")
		pieces = website.split(".")
		if (count == 0):
			print (website)
			continue
		#if "www" not in pieces[0] and "http" not in pieces[0]:
			#print(pieces[0])
		#	cleanWeb = pieces[0]
		else:
			for idx, p in enumerate(pieces):
					if "com" in p or "net" == p or "co" == p or "org" == p:
						pre = pieces[idx-1]
						if "www" not in pre and "http" not in pre:
							cleanWeb= pre
			if cleanWeb == None:
				if "www" not in pieces[0] and "http" not in pieces[0]:
					cleanWeb = pieces[0]
				else:	
					cleanWeb = pieces[1]

		#print (cleanWeb)
		#input("help")
		new_brand = Brand(brand_name=row[0], brand_website=website, brand_website_clean = cleanWeb)	
		session.add(new_brand)
	session.commit()

# for testing
#brand = session.query(Brand)
#for b in brand:
#	print(b.id, b.brand_name, b.brand_website)
