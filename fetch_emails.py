import imaplib
import email
import mailbox
import sys
sys.path.append('dbsetup')
from setup_db_SA import Email, Base, Brand
from parseBody import parseBody
from parse_image_links import parse_links
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

def fetchEmails(username, password):
#should we get email via ags?
    gmailbox = imaplib.IMAP4_SSL('imap.gmail.com')

    try:
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
	addEmailsToDB(mbox)
	print ('From', message['From'])

def matchEmailstoAddresses(email):
	pass

def addEmailsToDB(mbox):
    engine = create_engine('sqlite:///../emails2.db')
    Base.metadata.bind = engine

    DBSession = sessionmaker(bind=engine)
    session = DBSession()

    parse_links(mbox)
        
    for message in mbox:
        from_address = message['From']
        to_address = message['To']
        #print('To:', to_address)
        gmail_label = message['X-Gmail-Labels']
        #print('gmail labels:', gmail_label)
        time_sent = message['Date']
        #print ('time sent:', time_sent)
        message_id = message['Message-ID']
        #print ('message id:', message_id)
        #email_size = ...?
        subject_line = str(message['Subject'])
        #subject_line = subject_line.replace("�", "")
        #print('subject:', subject_line)
        #encode_sub = subject_line.encode('utf-8')
        #decode_subject = subject_line.decode('utf-8', 'ignore')
        #print('decoded: ', decode_subject)
        body_parser = parseBody() 
        body_plain = body_parser.getBody(message) 
        #print (body_plain[1:100])
        new_email = Email(sender_address=from_address, to_address=to_address,
                    time_sent=time_sent, message_id=message_id, subject_line=subject_line,
                    body_plain = body_plain)    

        session.add(new_email)
    session.commit()

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
