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
		new_brand = Brand(brand_name=row[0], brand_website=row[1])	
		session.add(new_brand)
	session.commit()

# for testing
#brand = session.query(Brand)
#for b in brand:
#	print(b.id, b.brand_name, b.brand_website)