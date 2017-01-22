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
		writer.writerow(['State', 'StateAbbr', 'Year', 'Client', 'Amount', 'Lobbyist1', 'Lobbyist2', 'Lobbyist3', 'Lobbyist4', 'Lobbyist5', 'Lobbyist6', 'Lobbyist7', 'Lobbyist8', 'Lobbyist9', 'Lobbyist10', 'Lobbyist11', 'Lobbyist12'])
		for row in data:
			writer.writerow(row)
	outcsv.close()

def getOptions(response, id):
	soup = BeautifulSoup(response.content, 'lxml')
	selector = soup.find('select', id=id)
	options = {}
	for x in selector.find_all("option"):
		options[x.text] = x.get("value")
	return options

def strip_money(value):
	value = value.replace("$", "")
	value = value.replace(",", "")
	value = value.replace(" ", "")
	return float(value)

def generateRow(response, year, companyName):
	soup = BeautifulSoup(response.content, 'lxml')
	table = soup.find('table', id="lobbyistList")
	
	allTds = table.find_all("td")
	length = len(allTds)
	sum = 0
	lobbyists = []

	if length == 0:
		return None

	for i in range(0, length//4):
		val = allTds[i*4]
		if val.a:
			lobbyists.append(val.a.text)
		else:
			lobbyists.append(val.text)

		sum += strip_money(allTds[i*4 + 3].text)

	row = ["Virginia", "VA", year, companyName, sum]
	row += lobbyists
	return row

if __name__ == "__main__":
	mainURL = "https://solutions.virginia.gov/Lobbyist/Reports/DisclosureSearch"
	formData = {"registrationYear":315880000, "principal":"fbf94291-a6a1-4a7b-a95e-a958bc83fd9d"}

	response = requests.post(mainURL, formData)
	soup = BeautifulSoup(response.content, 'lxml')
	
	selector = soup.find('select', id="registrationYear")
	years = []
	yearIds = []
	for x in selector.find_all("option"):
		years.append(x.text)
		yearIds.append(x.get("value"))
	
	selector = soup.find('select', id="principal")
	companies = []
	companyIds = []
	for x in selector.find_all("option"):
		companies.append(x.text)
		companyIds.append(x.get("value"))

	for i in range(6, len(years)):
		yearData = []
		for j in range(0, len(companies)):
			formData["registrationYear"] = yearIds[i]
			formData["principal"] = companyIds[j]

			response = requests.post(mainURL, formData)
			row = generateRow(response, years[i], companies[j])

			print(companies[j], years[i])
			if row:
				print(row)
				yearData.append(row)

		write_to_csv("../VA_{}.csv".format(years[i]), yearData)
		print("{} finished!".format(years[i]))

	print("FINISHED!!")
