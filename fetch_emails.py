import imaplib
import email
import mailbox
import sys
import csv

sys.path.append('dbsetup')
from setup_db_SA import Email, Base, Brand, Email_Address
from parseBody import parseBody
from parse_image_links import parse_links
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import select

engine = create_engine('sqlite:///emails2.db')
Base.metadata.bind = engine

DBSession = sessionmaker(bind=engine)
session = DBSession()

brands_dict = {}
unmatched = []
unmatchedIndex=0

def makeBrandDict():
    # create a dictionary of brands
    cleanwebs = session.query(Brand.id,Brand.brand_website_clean)
    #unind = session.query(Brand.id).filter(Brand.brand_name == "UNMATCHED")
    #unmatchedIndex = unind[0]
    #unmatchedIndex = unmatchedIndex[0]
    # the keys are tuplef of brand ids and names
    for clean in cleanwebs:
        brands_dict[(clean[0],clean[1])] = None


def fetchEmails(username, password):
    makeBrandDict()
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
        #print ('From', wholeEmail['From'])
        addEmailsToDB(wholeEmail)
    session.commit()


def fetchFromMbox(filename):
    makeBrandDict()
    mbox = mailbox.mbox(filename)
    #addEmailsToDB(mbox)

    count = 0
    for message in mbox:
        count +=1 
        #print (count)
        addEmailsToDB(message)
    session.commit()

    # for message in mbox:
    #     address = message['From']
    #     matchEmailstoAddresses(address)
    
    # pretty prints the brands_dict
    #for brand_entry in brands_dict.keys():
    #    if brands_dict[brand_entry] != None:
    #        printstr = ' '.join(map(str,brand_entry))
    #        printstr = printstr.rjust(30,' ')
            #print("\t",printstr, "   ", brands_dict[brand_entry])

def matchEmailstoAddresses(email):
    matched = False
    matches = []

    # finds match of the brand in the email, can have several
    for brand_entry in brands_dict.keys():
        clean = email.replace(".com","")
        if brand_entry[1] in clean:
            matches.append(brand_entry)
            matched = True;

    # cleans up the email address
    email = email.split('<')
    email = email[len(email)-1].strip('>')

    # if there are matches match to the longest brand name
    if matched:
        longest = matches[0]
        for match in matches:
            if (len(match[1]) > len(longest[1])):
                longest = match

        brands_dict[longest] = email
        return longest[0]

    # else add to list of unmatched brands
    else:
        unmatched.append(email)
        return unmatchedIndex ##UNMATCHED in the db is 1

def getAddress(address):
    try:
        eid = session.query(Email_Address.id).filter(Email_Address.email_address == address)
        eid = eid[0]
        return eid[0]
    except IndexError:
        brand_id = matchEmailstoAddresses(address)
        new_emailAddr = Email_Address(email_address=address, brand_id= brand_id)
        session.add(new_emailAddr)
        session.commit()
        getAddress(address)



def addEmailsToDB(message):
    # make social media parse call here
    #email_size = str(sys.getsizeof(mbox.get_bytes(message_count)))
    from_address = message['From']
    from_address = from_address.split('<')
    from_address = from_address[len(from_address)-1].strip('>')
    address_id = getAddress(from_address)
    #print(address_id)
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
    all_links, social_links = parse_links(body_plain)
    #print (body_plain)
    new_email = Email(sender_address=from_address, address_id=address_id, to_address=to_address,
                time_sent=time_sent, message_id=message_id, subject_line=subject_line,
                body_plain = body_plain, body_links = str(all_links), social_links = str(social_links))
    session.add(new_email)
    #session.commit()


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
