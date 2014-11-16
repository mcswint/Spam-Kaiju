import re

def parse_links(message):
    #find any link and print it out
    list = []
    for key,value in message.items():
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value)
        list.extend(urls)
    if list:
        print(list)
    
