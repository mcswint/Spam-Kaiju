import mailbox
import sys
from html.parser import HTMLParser

class MyHTMLParser(HTMLParser):
    def __init__(self): 
        super().__init__()
        self.datastring = ""

    def handle_data(self, data):
        self.datastring += data
        
    def getDatastring(self):
        return self.datastring


class parseBody():
    def getcharsets(self, msg):
        #get charsets contained in email
        charsets = set({})
        for c in msg.get_charsets():
            if c is not None:
                charsets.update([c])
        return charsets

    def decode(self, msg, body):
        #for each charset in email, try to decode
        for charset in self.getcharsets(msg):
            try:
                body = body.decode(charset)
            except UnicodeDecodeError:
                continue    
            except AttributeError:
                continue
        return body    

    def convertHTML(self, msg):
        #if msg is html type, decode first, then parse html
        body = msg.get_payload(decode=True)
        
        if (body != None):
            body = self.decode(msg, body)
            parser = MyHTMLParser()
            parser.feed(str(body))
            parsed = parser.getDatastring()
            return parsed
        else:
            return ""

    #takes in msg and returns body in text format
    def getBody(self, msg):
        body = None
        #if msg is multipart, walk through each section to find the text 
        if msg.is_multipart():    
            for part in msg.walk():

                #if the part is multipart, go through each part of the email
                #to find the text
                if part.is_multipart(): 

                    for subpart in part.walk():
                        if subpart.get_content_type() == 'text/plain':
                            body = subpart.get_payload(decode=True) 
                            return self.decode(msg, body)   

                        elif subpart.get_content_type() == 'text/html':
                            return self.convertHTML(msg)

                # Part isn't multipart so get the email body
                elif part.get_content_type() == 'text/plain':
                    body = part.get_payload(decode=True)
                    return self.decode(msg, body) 

                elif part.get_content_type() == 'text/html':
                    return self.convertHTML(msg)      

        elif msg.get_content_type() == 'text/plain':
            body = msg.get_payload(decode=True) 
            return self.decode(msg,body)

        elif msg.get_content_type() == 'text/html':
            return self.convertHTML(msg)