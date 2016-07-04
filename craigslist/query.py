import requests
from datetime import datetime
from dateutil import parser as dtparser
import smtplib
import os


from bs4 import BeautifulSoup as bs4

def parse (entry):
	price = entry.find('span',attrs={'class': 'price'})
	if (price is not None):
		price=price.text
	else:
		price="$0"
	time = entry.find('time')
	if (time is not None):
		time = time['datetime']
	else:
		time=""
	title = entry.find('a', attrs={'class': 'hdrlnk'})
	if (title is not None):
		title=title.text
	else:
		title=""
	id = entry['data-pid']
	href = entry.find('a', attrs={'class': 'hdrlnk'})
	if (href is not None):
		href=href['href']
	else:
		href=""
	if (href.startswith ('//')):
		href= 'http:' + href
	else:
		href = 'http://atlanta.craigslist.org' + href


	#dt = dtparser.parse(time)

	return price,time,title,id,href

def sendMail(to,sub,body):
    sendmail_location = "/usr/sbin/sendmail" # sendmail location
    p = os.popen("%s -t" % sendmail_location, "w")
    p.write("From: %s\n" % "noreply@hasanzadeh.com")
    p.write("To: %s\n" % to)
    p.write("Subject: "+sub+"\n")
    p.write("\n") # blank line separating headers from body
    p.write(body)
    status = p.close()



with open('found.txt','r') as f:
	found = [x.strip() for x in f.readlines()]

with open('requests.txt','r') as f:
	for line in f:
		line = line.strip()
		columns = line.split()
		url = columns[0]
		email= columns[1]


		rsp = requests.get(url)
		html = bs4(rsp.text, 'html.parser')
		entries= html.find_all('p', attrs={'class': 'row'})

		for entry in entries:
			price,time,title,id,href = parse(entry)
			if (id not in found):
				print ('New found '+id)
				with open("found.txt", "a") as myfile:
				    myfile.write(id+"\n")
				msg ="Hello,\nA New item has been found at: "+href+"\nThank you!\n";
				sub='CRG:#'+title+" "+price
				sendMail(email,sub,msg)




