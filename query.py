import requests
from datetime import datetime
from dateutil import parser as dtparser
import smtplib
import os


from bs4 import BeautifulSoup as bs4

def parse (entry):
	price = entry.findAll('span',attrs={'class': 'price'})[0].text
	time = entry.find('time')['datetime']
	title = entry.find('a', attrs={'class': 'hdrlnk'}).text

	print (price + ' ' + time + ' ' + title)
	dt = dtparser.parse(time)
	print (dt <= dt)

def sendMail(to,sub,body):
    sendmail_location = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % sendmail_location, "w")
    p.write("From: %s\n" % "noreply@hasanzadeh.com")
    p.write("To: %s\n" % to)
    p.write("Subject: "+sub+"\n")
    p.write("\n") # blank line separating headers from body
    p.write(body)
    status = p.close()


sendMail('ha.hassanzadeh@gmail.com','Test 9','Hi')

url = 'http://atlanta.craigslist.org/search/sso';
params=dict(query='gtx',sort='date',hasPic=1,max_price=125);
rsp = requests.get(url, params=params)

html = bs4(rsp.text, 'html.parser')

# BS makes it easy to look through a document
entries= html.find_all('p', attrs={'class': 'row'})
print (entries[0])
for entry in entries:
	parse(entry)


