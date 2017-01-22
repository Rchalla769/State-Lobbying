import requests
import json
from bs4 import BeautifulSoup
import csv
from os import path
import os
import string

baseUrl = 'http://nebraskalegislature.gov/lobbyist/'
data = {}

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

def parse_client_pages(links):
	for link in links:
		link = "{}{}".format(baseUrl, link['href'])
		response = requests.get(link)
		soup = BeautifulSoup(response.content, 'lxml')
		selectElement = soup.find("select", {'name': 'Year'})
		options = selectElement.find_all("option")
		years = [option.text for option in options][1:]
		parse_year_pages(years, link)

def parse_year_pages(years, link):
	for year in years:
		response = requests.post(link, data={'Year':year})
		soup = BeautifulSoup(response.content, 'lxml')
		links = soup.find_all("a", {'class', 'list-group-item'})
		clientName = soup.find("span", {'id': 'PrincipalName'}).text
		quarterLinks = []
		for l in links:
			if 'formc' in l['href']:
				quarterLinks.append("{}{}".format(baseUrl, l['href']))
		parse_quarter_pages(clientName, year, quarterLinks)

def parse_quarter_pages(clientName, year, links):
	print(clientName, year)
	for link in links:
		response = requests.get(link)
		soup = BeautifulSoup(response.content, 'lxml')
		lobbyists = soup.find('p', {'id': 'Lobbyists'}).text.replace('\n', '').strip()
		amount = float(soup.find('p', {'id': 'TotalExpenses'}).text.replace(',', ''))
		
		if year in data:
			if clientName in data[year]:
				data[year][clientName]["amount"] += amount
				if lobbyists not in data[year][clientName]["lobbyists"]:
					data[year][clientName]["lobbyists"].append(lobbyists)
			else:
				data[year][clientName] = {'amount': amount, 'lobbyists': [lobbyists]}
		else:
			data[year] = {clientName: {'amount': amount, 'lobbyists': [lobbyists]}}
		
if __name__ == "__main__":
	list_range = [1]
	list_range += list(string.ascii_uppercase)

	for listVal in list_range:
		response = requests.get("{}view.php?v=principal&list={}".format(baseUrl, listVal))
		soup = BeautifulSoup(response.content, 'lxml')
		table = soup.find("table", {"class": "table table-condensed"})
		parse_client_pages(table.find_all("a"))

	for (year, clients) in data.items():
		rows = []
		for (client, info) in clients.items():
			row = ["Nebraska", "NE", year, client, info["amount"]]
			row += info["lobbyists"]
			rows.append(row)
		write_to_csv("../NE_{}.csv".format(year), rows)
		print("{} finished!!".format(year))
	print("ALL DONE!!")