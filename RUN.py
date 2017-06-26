import sys
reload(sys)
sys.setdefaultencoding('utf8')

import re

import requests
from bs4 import BeautifulSoup as bs
import csv

import os.path
my_path = os.path.abspath(os.path.dirname(__file__))

#path to save the result
path = os.path.join(my_path, "result.csv")

#Input the Search Item:
search_item = raw_input("Input The Search Item: ")

#Input The Location
loc = raw_input("Input The Location: ")

location = ""
for i in loc:
    if (i == " "):
        location += "%20"
    elif (i == ","):
        location += "%2C"
    else:
        location += i

page_number = 1

base_url = "https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + location + "&page=" + str(page_number)

r = requests.get(base_url)

soup = bs(r.content, 'html.parser')

g_data = soup.find_all('div', {"class": "info"})

header = []
address = []
phone_number = []

for i in range(2,30):
    item = g_data[i]
    header.append("".join(list((item.contents[0].find_all('a')[0].text).encode('utf-8'))))
    address.append("".join(list((item.contents[1].find_all('p', {"class": "adr"})[0].text).encode('utf-8'))))
    phone_number.append("".join(list((item.contents[1].find_all('div', {"itemprop": "telephone"})[0].text).encode('utf-8'))))

    info = zip(header, address, phone_number)

    with open(path, "w") as csv_file:
        SourceFileWriter = csv.writer(csv_file)
        SourceFileWriter.writerow([search_item.upper()+", "+loc.upper(), "ADDRESS", "Phone-Number"])
        
        for i in info:
            SourceFileWriter.writerow(list(i))
    
    csv_file.close()
