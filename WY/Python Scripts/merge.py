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
		writer.writerow(['State', 'StateAbbr', 'Year', 'Client', 'Lobbyist1', 'Lobbyist2', 'Lobbyist3', 'Lobbyist4', 'Lobbyist5', 'Lobbyist6', 'Lobbyist7', 'Lobbyist8', 'Lobbyist9', 'Lobbyist10', 'Lobbyist11', 'Lobbyist12'])
		for row in data:
			writer.writerow(row)
	outcsv.close()

def create_dict(filename):
	with open(filename) as csvfile:
		reader = csv.reader(csvfile, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		data = {}
		for row in reader:
			if row[1] in data:
				data[row[1]].append(row[0])
			else:
				data[row[1]] = [row[0]]
		return data

if __name__ == "__main__":
	years = [1998, 1999, 2000, 2001, 2002, 2003, 2004, 2005, 2006, 2007, 2008,
			2009, 2010, 2011, 2012, 2013]

	for year in years:
		filename = "../Raw Data/unorganized_{}.csv".format(year)
		data = create_dict(filename)

		rows = []

		for key in data:
			vals = data[key]

			new_row = []
			new_row.append("Wyoming")
			new_row.append("WY")
			new_row.append(year)
			new_row.append(key)
			new_row += vals
			rows.append(new_row)

		newFile = "../WY_{}.csv".format(year)
		write_to_csv(newFile, rows)
