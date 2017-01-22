#Author: Rohan Challa
#Email: rchalla@stanford.edu
#Date: October 09, 2016

from os import path
import os
import csv
from bs4 import BeautifulSoup

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

def groupLobbyists(data):
	lobby_dict = {}
	for row in data:
		if row[1] in lobby_dict:
			salary = row[3]
			if "$" in salary:
				salary = salary.replace("$","")
			if "," in salary:
				salary = salary.replace(",", "")
			lobby_dict[row[1]]["amount"] += float(salary)
			if (row[2] != "N/A") and (row[2] not in lobby_dict[row[1]]["lobbyists"]):
				lobby_dict[row[1]]["lobbyists"].append(row[2])
		else:
			salary = row[3]
			if "$" in salary:
				salary = salary.replace("$","")
			if "," in salary:
				salary = salary.replace(",", "")
			lobby_dict[row[1]] = {"year": row[0], "amount": float(salary), "lobbyists": []}
			if row[2] != "N/A":
				lobby_dict[row[1]]["lobbyists"] = [row[2]]
	
	toReturn = []
	for key,value in lobby_dict.items():
		row = []
		row.append("Mississippi")
		row.append("MS")
		row.append(value["year"])
		row.append(key)
		row.append(value["amount"])
		row += value["lobbyists"]
		toReturn.append(row)
	return toReturn

if __name__ == '__main__':
	years = ["2011", "2012", "2013", "2014", "2015", "2016"]
	for year in years:
		with open(("../2011-2016/" + year + ".htm")) as f:
			soup = BeautifulSoup(f, 'html.parser')
			all_td = soup.find_all('td')

			data_rows = []

			row = []

			count = 0

			form_c = ["Form C", "Form C - Termination"]

			while count < len(all_td):
				if all_td[count].string in form_c:
					count += 2
					subCount = 0
					while count < len(all_td) and all_td[count].string not in form_c:
						row.append(all_td[count].string)
						count += 1
					data_rows.append(row)
					row = []
				else:
					count += 1
			write_to_csv("../MS_" + year + ".csv", groupLobbyists(data_rows))