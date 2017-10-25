import requests
import re
from bs4 import BeautifulSoup
import csv
import geocoder
import logging

url='https://www.wgzimmer.ch/wgzimmer/search/mate.html?query=&priceMin=50&priceMax=1500&state=zurich-stadt&permanent=all&student=none&country=ch&orderBy=MetaData%2F%40mgnl%3Alastmodified&orderDir=descending&startSearchMate=true&wgStartSearch=true'
domain='http://www.wgzimmer.ch'
csv_file = open("rent.csv", "w")
csv_writer = csv.writer(csv_file, delimiter=',')
r=requests.get(url)
soup=BeautifulSoup(r.content,'html.parser')
house=soup.find_all(class_="list")[0].find_all("a")
house=[h for i,h in enumerate(house) if i % 2 ==1]
for h in house[:100]:
	link=h.get('href')
	link="".join([domain,link])
	r=requests.get(link)
	soup=BeautifulSoup(r.content,'html.parser')
	info = soup.find_all(class_="wrap col-wrap date-cost")[0].find_all('p')
	start_date = info[0].text.replace('Ab dem ','')
	end_date = info[1].text.replace('Bis ','')
	price=info[2].text.replace('Miete ', '').replace('/ Monat ','').replace('.-','')
	addr=soup.find_all(class_="wrap col-wrap adress-region")[0]
	location = addr.find_all('p')[1].text.replace('Adresse ','')
	try:
		ll=geocoder.google(','.join([location,'zurich'])).latlng
		latlong=' '.join([str(ll[0]), str(ll[1])])
		csv_writer.writerow([location, price, start_date, end_date, link, latlong])
	except Exception as e:
		logging.error('errors of geocoding', exc_info=True)
		csv_writer.writerow([location, price, start_date, end_date, link])

csv_file.close()
