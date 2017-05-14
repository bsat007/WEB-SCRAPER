import requests
from bs4 import BeautifulSoup as bs
import csv


def convert_to_str(ss):
    i = 0
    x = ""
    while (i < len(ss)):
        if (ss[i] == '\xc2'):
            i += 2
        else:
            x += ss[i]
            i += 1
    return x


search_item = raw_input("Input The Search Item: ")
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

base_url = "https://www.yellowpages.com/search?search_terms=" + search_item + "&geo_location_terms=" + location + "&page=" + str(
    page_number)

r = requests.get(base_url)

soup = bs(r.content, 'html.parser')

g_data = soup.find_all('div', {"class": "info"})

header = []
address = []
phone_number = []

for i in range(2,30):
    item = g_data[i]
    header.append(convert_to_str(list((item.contents[0].find_all('a')[0].text).encode('utf-8'))))
    address.append(convert_to_str(list((item.contents[1].find_all('p', {"class": "adr"})[0].text).encode('utf-8'))))
    phone_number.append(convert_to_str(list((item.contents[1].find_all('div', {"itemprop": "telephone"})[0].text).encode('utf-8'))))

    h1 = []
    h2 = []
    h3 = []

    info = zip(header, address, phone_number)

    with open("/Users/badalsatyarthi/PycharmProjects/WEB_Scrapping/test.csv", "w") as csv_file:
        SourceFileWriter = csv.writer(csv_file)

        for i in info:
            SourceFileWriter.writerow(list(i))
    csv_file.close()
