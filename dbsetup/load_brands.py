import sqlite3
import csv
import sys


conn = sqlite3.connect("../emails.db")

with conn:
	cur = conn.cursor()

	with open('brands_and_websites.csv') as datafile:
		data = csv.reader(datafile, delimiter=',')
		for row in data:
			
			stmt = 'INSERT INTO brand (brand_name, brand_website) VALUES ("{0}", "{1}")'.format(row[0], row[1])

			cur.execute(stmt)

	#for testing
	#cur.execute('SELECT * FROM brand')
	#res = cur.fetchall()
	#print (res)