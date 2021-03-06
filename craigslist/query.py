import requests
import time
import sys
import random
from datetime import datetime
from dateutil import parser as dtparser
import smtplib
import os
from bs4 import BeautifulSoup as bs4
import mylib


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
		#href= 'http:' + href
		href= ''
	else:
		href = 'http://atlanta.craigslist.org' + href


	#dt = dtparser.parse(time)

	return price,time,title,id,href

def query(url,proxy,email,timeout=20):
	#rsp = requests.get(url,headers={"content-type":"text"},proxies={'http': 'http://' + proxy}, timeout=timeout)
	rsp = requests.get(url,headers={"content-type":"text"},proxies={'http': 'http://' + proxy,'https': 'https://' + proxy}, timeout=timeout)
	#rsp = requests.get(url,headers={"content-type":"text"},proxies={'http': 'http://' + proxy} )
	#rsp = requests.get(url,proxies={'http': 'http://' + proxy}, timeout=timeout)
	html = bs4(rsp.text, 'html.parser')
	entries= html.find_all('p', attrs={'class': 'row'})
	for entry in entries:
		price,time,title,id,href = parse(entry)
		if (href == ''):
			continue
		if (id+':'+time not in found):
			print ('New found '+id)
			with open("/home/hamidreza/web-dev/craigslist/found.txt", "a") as myfile:
			    myfile.write(id+':'+time+"\n")
			msg ="Hello,\nA new item has been found at: "+href+"\nThank you!\n";
			sub='CRG:#'+title+" "+price
			mylib.sendMail(email,sub,msg)
	#print ('Success'+proxy)





with open('/home/hamidreza/web-dev/craigslist/found.txt','r') as f:
	found = [x.strip() for x in f.readlines()]
with open('/home/hamidreza/web-dev/craigslist/verified_proxies.txt','r') as f:
	proxies= [x.strip() for x in f.readlines()]
if (len(proxies)<15):
	sys.exit('Error number of proxies is small!')

with open('/home/hamidreza/web-dev/craigslist/requests.txt','r') as f:
	for line in f:
		line = line.strip()
		columns = line.split()
		url = columns[0]
		email= columns[1]

		proxy =random.choice(proxies)
		timeout=20

		try:
			query(url,proxy,email,timeout)
		except:
			try:
				proxy =random.choice(proxies)
				query(url,proxy,email,timeout)
			except:
				try:
					proxy =random.choice(proxies)
					query(url,proxy,email,timeout)
				except:
					#print ('Exception occured! '+proxy)
					continue

