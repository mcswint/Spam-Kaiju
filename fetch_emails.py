import imaplib
import email
import mailbox
import sys
sys.path.append('dbsetup')
from setup_db_SA import Email, Base, Brand


from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def fetchEmails(username, password):
	#should we get email via ags?
	gmailbox = imaplib.IMAP4_SSL('imap.gmail.com')

	try: 
		#mailbox.login('michellecastillo1989@gmail.com', 'l2thinktank')
		gmailbox.login(username, password)
	except imaplib.IMAP4.error:
		print ("login not successful")
		sys.exit(0)

	#pull all the message numbers
	status, box = gmailbox.select("INBOX")
	status, msgNum = gmailbox.search(None, "ALL")

	for m in msgNum[0].split():
		#gets individual email by number
		status, theEmail = gmailbox.fetch(m, '(RFC822)')
		if status != 'OK':
			print ("Message Error", m)
			return
		# uses email class to parse the email
		wholeEmail = email.message_from_bytes(theEmail[0][1])
		#you can access each part like a dict
		print ('From', wholeEmail['From'])


def fetchFromMbox(filename):
	mbox = mailbox.mbox(filename)
	for message in mbox:
		print ('From', message['From'])

def matchEmailstoAddresses(email):
	pass		

def addEmailsToDB(message):


def main(argv):
	if (len(argv) ==1):
		fetchFromMbox(argv[0])
	elif (len(argv) ==2):
		fetchEmails(argv[0], argv[1])
	else:
		print ("Incorrect number of args")
		sys.exit(0)
	


if __name__ =='__main__':
    main(sys.argv[1:])