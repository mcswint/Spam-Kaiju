import re
import types
def parse_links(message):
    #find any link and print it out
    list = []
    for key,value in message.items():
        if type(value) is str:
            urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', value)
            list.extend(urls)
    if list:
        parse_social_media(list)
        return(list)
def parse_social_media(list):
    #find any link and print it out
    social_media = []
    links_to_check = ["petco"]
    for link_string in list:
        #any(substring in string for substring in substring_list)
        if any(substring in link_string for substring in links_to_check):
            print(link_string)