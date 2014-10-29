##command to set up db tables
## do not run if db already exsists!

import sqlite3

conn = sqlite3.connect("../emails.db")

with conn:
	cur = conn.cursor()
	conn.execute('PRAGMA foreign_keys = ON')
	cur.execute("CREATE TABLE brand (brand_id INTEGER PRIMARY KEY, brand_name TEXT, brand_website TEXT)")
	cur.execute("CREATE TABLE email_address (email_address_id INTEGER PRIMARY KEY, email_address_name TEXT)")
	cur.execute("CREATE TABLE brand_to_email_address(brand_id INT, email_address_id INT, \
		FOREIGN KEY(brand_id) REFERENCES brand(brand_id), FOREIGN KEY(email_address_id) REFERENCES \
		email_address(email_address_id))")
	cur.execute("CREATE TABLE email (email_id INTEGER PRIMARY KEY, email_address_id INT, sender_address TEXT, \
		to_address TEXT, gmail_label TEXT, time_sent TEXT, email_message_id TEXT, email_size INT, subject_line TEXT, \
		body_text TEXT, body_plain TEXT, body_links TEXT, body_images TEXT, FOREIGN KEY(email_address_id) REFERENCES \
		email_address(email_address_id))")
	cur.execute("CREATE TABLE email_fact_by_brand(record_id INTEGER PRIMARY KEY, fact_date TEXT, brand_id INT, \
		email_frequency REAL, most_common_word_in_sub TEXT, per_contain_social_links, sent_bday_email TEXT,\
		FOREIGN KEY(brand_id) REFERENCES brand(brand_id))")
