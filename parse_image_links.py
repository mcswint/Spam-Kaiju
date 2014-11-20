import re
import types
def parse_links(message):
    #find any link and print it out
    list = []
    if type(message) is str:
        urls = re.findall('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+', message)
        list.extend(urls)
    social_media_links = parse_social_media(list)
    return(list, social_media_links)

def parse_social_media(list):
    #find any link and print it out
    social_media = []
    links_to_check = ["facebook", "twitter"]
    for link_string in list:
        if any(substring in link_string for substring in links_to_check):
            social_media.append(link_string)
    return social_media
