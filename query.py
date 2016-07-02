import requests
from datetime import datetime
from dateutil import parser as dtparser
import smtplib


from bs4 import BeautifulSoup as bs4

def parse (entry):
	price = entry.findAll('span',attrs={'class': 'price'})[0].text
	time = entry.find('time')['datetime']
	title = entry.find('a', attrs={'class': 'hdrlnk'}).text

	print (price + ' ' + time + ' ' + title)
	dt = dtparser.parse(time)
	print (dt <= dt)


url = 'http://atlanta.craigslist.org/search/sso';
params=dict(query='gtx',sort='date',hasPic=1,max_price=125);
rsp = requests.get(url, params=params)

html = bs4(rsp.text, 'html.parser')

# BS makes it easy to look through a document
entries= html.find_all('p', attrs={'class': 'row'})
print (entries[0])
for entry in entries:
	parse(entry)


