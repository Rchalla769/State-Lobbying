#Author: Rohan Challa
#Email: rchalla@stanford.edu
#Date: October 14, 2016

import csv
from os import path
import os

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

def get_total_spending(row):
	total = 0
	for i in range(0, 12):
		value = row[i*4 + 14]
		if "$" in value:
			value = value.replace("$","")
		if "," in value:
			value = value.replace(",", "")

		try:
			total += float(value)
		except ValueError:
			total += 0
	return total

if __name__ == '__main__':
	years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]

	for year in years:
		with open(("../Raw Data/IA_" + year + ".csv")) as csvfile:
			reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			data = []
			for row in reader:
				if row[0] == "Client":
					continue
				new_row = []
				new_row.append("Iowa")
				new_row.append("IA")
				new_row.append(year)
				new_row.append(row[0].strip())
				new_row.append(get_total_spending(row))
			
				for i in range(0, 12):
					value = row[i*4 + 11].strip()
					if not value.isspace():
						new_row.append(value)
				data.append(new_row)
			write_to_csv("../IA_"+year+".csv", data)
		csvfile.close()