from os import path
import os
import csv
import ast

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

if __name__ == "__main__":
	with open("test.txt") as f:
		lines = f.readlines()
		data = []

		for line in lines:
			if line[0] == "[":
				line = line.replace("\n", "")
				data.append(ast.literal_eval(line))

		print(data)

		write_to_csv("../Raw Data/2011-2012.csv", data)

