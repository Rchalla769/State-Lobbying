import requests
from bs4 import BeautifulSoup
from os import path
import os
import csv

def write_to_csv(filename, data):
	#try statement to remove previous file before writing new file
	try:
		os.remove(filename)
	except OSError:
		pass
		
	with open(filename, 'a') as outcsv:
		#Specialized writer object to write to a csv file
		writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		writer.writerow(['State', 'StateAbbr', 'Year', 'Client', 'Amount', 'Lobbyist1', 'Lobbyist2', 'Lobbyist3', 'Lobbyist4', 'Lobbyist5', 'Lobbyist6', 'Lobbyist7', 'Lobbyist8', 'Lobbyist9', 'Lobbyist10', 'Lobbyist11', 'Lobbyist12'])
		for row in data:
			writer.writerow(row)
	outcsv.close()

def reverse_name(name):
	names = name.split(', ')
	return '{} {}'.format(names[1], names[0])

def strip_dollars(dollar):
	dollar = dollar.replace('$', '')
	dollar = dollar.replace(',', '')
	return dollar

def parse_body(body, name, year, data):
	rows = []
	noRecords = body.find('tr', {'class':'rgNoRecords'})
	if noRecords is None:
		trs = body.find_all('tr')
		for tr in trs:
			tds = tr.find_all('td')
			client = tds[0].text
			dollar = tds[-1].text
			if '$' in dollar:
				dollar = float(strip_dollars(dollar))
			else:
				dollar = 0
			data = add_to_dict(data, name, year, client, dollar)
	return data

def add_to_dict(data, name, year, client, amount):
	if client in data[year]:
		if name not in data[year][client]['lobbyists']:
			data[year][client]['lobbyists'].append(name)
		data[year][client]['amount'] += amount
	else:
		data[year][client] = {'lobbyists': [name], 'amount': amount}
	return data

if __name__ == "__main__":
	baseUrl = 'https://sos.sd.gov/Lobbyist/LRPublicAccess.aspx'
	currentSession = requests.Session()
	response = currentSession.get(baseUrl)
	soup = BeautifulSoup(response.content, 'lxml')

	viewState = soup.find("input", {"id":"__VIEWSTATE"}).get("value")
	viewStateGenerator = soup.find("input", {"id":"__VIEWSTATEGENERATOR"}).get("value")
	eventValidation = soup.find("input", {"id":"__EVENTVALIDATION"}).get("value")

	formData = {
		'ctl00_RadScriptManager1_TSM':';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:4bd8faf8-554d-46be-b2ff-c9d57adb612c:ea597d4b:b25378d2;Telerik.Web.UI, Version=2014.1.403.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:ca584452-327f-4858-bf00-fb22c6f6fd75:16e4e7cd:f7645509:ed16cbdc:88144a7a:24ee1bba:7165f74:e330518b:1e771326:8e6f0d33:6a6d718d:f46195d3:2003d0b8:aa288e2d:258f1c72:b7778d6c:58366029',
		'__EVENTTARGET': '',
		'__EVENTARGUMENT': '',
		'__VIEWSTATE': viewState,
		'__VIEWSTATEGENERATOR': viewStateGenerator,
		'__EVENTVALIDATION': eventValidation,
		'ctl00_MainContent_btnHomepge_ClientState':'',
		'ctl00_MainContent_RadTabStripSearchOptions_ClientState':'{"selectedIndexes":["0"],"logEntries":[],"scrollState":{}}',
		'ctl00$MainContent$cboSessionsPriSearch':'All Years',
		'ctl00_MainContent_cboSessionsPriSearch_ClientState':'',
		'ctl00$MainContent$txtWordSearch':'Enter a Word to Search for',
		'ctl00_MainContent_txtWordSearch_ClientState':'{"enabled":true,"emptyMessage":"Enter a Word to Search for","validationText":"","valueAsString":"","lastSetTextBoxValue":"Enter a Word to Search for"}',
		'ctl00$MainContent$cboWordSearchType':'Wildcard-Default: This finds all words or partial words that match what you entered.',
		'ctl00_MainContent_cboWordSearchType_ClientState':'',
		'ctl00$MainContent$btnPriSearch':'Go',
		'ctl00_MainContent_radGrdPriSearchResults_ClientState':'',
		'ctl00$MainContent$cboSessionsPrivatePrint':'2017',
		'ctl00_MainContent_cboSessionsPrivatePrint_ClientState':'',
		'ctl00$MainContent$cboSessionsPubSearch':'All Years',
		'ctl00_MainContent_cboSessionsPubSearch_ClientState':'',
		'ctl00_MainContent_radgrdPublic_ClientState':'',
		'ctl00$MainContent$cboSessionsPublicPrint':'2017',
		'ctl00_MainContent_cboSessionsPublicPrint_ClientState':'',
		'ctl00_MainContent_RadMultiPageSearchType_ClientState':'',
		'ctl00$MainContent$hdfpreviousTab':'' 
		}

	data = {} 

	for i in range(0, 8):
		print('Page {} Started!'.format(i+1))
		response = currentSession.post('https://sos.sd.gov/Lobbyist/LRPublicAccess.aspx', formData)
		soup = BeautifulSoup(response.content, 'lxml')

		div = soup.find('div', {'class', 'RadGrid RadGrid_Default'})
		links = div.find_all('a')
		hrefs = []
		names = []
		for link in links:
			href = link.get('href')
			if href and 'Lobbyist' in href:
				hrefs.append(href)
				names.append(reverse_name(link.text))

		for i in range(0, len(hrefs)):
			url = '{}{}'.format('https://sos.sd.gov/Lobbyist/', hrefs[i])
			response = requests.get(url)
			soup2 = BeautifulSoup(response.content, 'lxml')
			bodys = soup2.find_all('tbody')
			yearDiv = soup2.find('input', {'id': 'ctl00_MainContent_txtLegSession'})
			year = 2019

			if yearDiv is not None:
				yearDiv.get('value')

			if year not in data:
				data[year] = {}

			data = parse_body(bodys[-1], names[i], year, data)
			data = parse_body(bodys[-2], names[i], year, data)

		viewState = soup.find("input", {"id":"__VIEWSTATE"}).get("value")
		viewStateGenerator = soup.find("input", {"id":"__VIEWSTATEGENERATOR"}).get("value")
		eventValidation = soup.find("input", {"id":"__EVENTVALIDATION"}).get("value")

		if 'ctl00$MainContent$btnPriSearch' in formData:
			del formData['ctl00$MainContent$btnPriSearch']
		formData['ctl00$MainContent$radGrdPriSearchResults$ctl00$ctl03$ctl01$ctl22'] = '' 
		formData['ctl00$MainContent$radGrdPriSearchResults$ctl00$ctl03$ctl01$PageSizeComboBox'] = '500'
		formData['ctl00_MainContent_radGrdPriSearchResults_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState'] = ''
		formData['__VIEWSTATE'] = viewState
		formData['__VIEWSTATEGENERATOR'] = viewStateGenerator
		formData['__EVENTVALIDATION'] = eventValidation

	for (year, clients) in data.items():
		rows = []
		for (client, info) in clients.items():
			row = ["South Dakota", "SD", year, client, info["amount"]]
			row += info["lobbyists"]
			rows.append(row)
		write_to_csv("../SD_{}.csv".format(year), rows)
		print("{} finished!!".format(year))
	print("ALL DONE!!")



