import requests
from bs4 import BeautifulSoup
from os import path
import os
import csv

# Function to write the data to the appropriate filename
def write_to_csv(filename, data):
	#try statement to remove previous file before writing new file
	try:
		os.remove(filename)
	except OSError:
		pass
		
	with open(filename, 'a') as outcsv:
		#Specialized writer object to write to a csv file
		writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		for row in data:
			writer.writerow(row)
	outcsv.close()

def extract_information(lines, year):
	space_char = '\xa0'
	data = []
	currentCompany = ""

	newLines = []
	for line in lines:
		lineText = line.get_text()
		if lineText is not None:
			newLines += lineText.split("\n")

	allRows = []
	row = ['State', 'StateAbbr', 'Year', 'Client', 'Lobbyist1', 'Lobbyist2', 'Lobbyist3', 'Lobbyist4', 'Lobbyist5', 'Lobbyist6', 'Lobbyist7', 'Lobbyist8', 'Lobbyist9', 'Lobbyist10', 'Lobbyist11', 'Lobbyist12']		
	for line in newLines:
		listText = list(line)
		if len(listText) > 2:
			if listText[0] == space_char and (listText[1] != space_char and listText[1] != ' '):
				allRows.append(row)
				del listText[0]
				row = ["North Dakote", "ND", year, "".join(listText)]
			elif len(listText) > 11 and listText[10] == '#':
				name = "".join(listText[15:])
				name = name.replace('\xa0', '')
				name = name.split(", ")

				if len(name) < 2:
					name = "".join(name).split(" ")

				if len(name) > 1:
					row.append("{} {}".format(name[1], name[0]))
				else:
					row.append(name[0])

	return allRows


if __name__ == "__main__":
	#Years 2012-2017, add more if need be
	years = [2012, 2013, 2014, 2015, 2016]

	for year in years:
		if year == 2016: #handle special url for 2016
			url = "http://sos.nd.gov/lobbyists/registered-lobbyists/2016-organizations-lobbyists"
			response = requests.get(url)

			soup = BeautifulSoup(response.content, 'lxml')
			allDivs = soup.find_all("div", {'class':None, 'id':None})
			data = extract_information(allDivs, year)
		else:
			url = "http://sos.nd.gov/lobbyists/registered-lobbyists/{}-organizations-listed-alphabetically-lobbyists".format(year)
			response = requests.get(url)

			soup = BeautifulSoup(response.content, 'lxml')
			allPs = soup.find_all("p")
			del allPs[0] #remove the first element since it is a descriptor
			data = extract_information(allPs, year)
		write_to_csv("../ND_{}.csv".format(year), data)
		print("Finished {}!!".format(year))

			