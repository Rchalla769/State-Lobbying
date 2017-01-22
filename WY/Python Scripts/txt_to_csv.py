# Use http://document.online-convert.com/convert-to-txt to convert pdf to .txt
# Then run this program to turn .txts into .csvs.
# This program does not run perfectly since the .txt files are not formatted the same, so after 
# running this program, there needs to be some error checking.
from os import path
import os
import csv

# Function to write the data to the appropriate filename
def write_to_csv(filename, data, header):
	#try statement to remove previous file before writing new file
	try:
		os.remove(filename)
	except OSError:
		pass
		
	with open(filename, 'a') as outcsv:
		#Specialized writer object to write to a csv file
		writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		writer.writerow(header)
		for row in data:
			writer.writerow(row)
	outcsv.close()

def parse_1998():
	year = 1998
	filename = "../Raw Data/txts/1998-1999_WY_Lobbyist_List.txt"
	currentRow = 0
	lobbyistNameDelimiters = ["Lobbyist Name\n", "Lobbyist Name Address\n"]

	with open(filename) as txtFile:
		reader = txtFile.readlines()

	outputData = []
	currentLobbyName = ""

	while currentRow < len(reader):
		row = reader[currentRow]
		if "Lobbyist Name" in row:
			if row not in lobbyistNameDelimiters:
				row = reader[currentRow]
			else:
				row = reader[currentRow+1]
			currentLobbyName = row.replace("\n", "")
		elif "Organization Information" in row:
			if "Address, City, State and Zip" in reader[currentRow+1]:
				row = reader[currentRow+3]
			else:
				row = reader[currentRow+1]
			outputData.append([currentLobbyName, row.replace("\n", "")])
		currentRow += 1

	header = ["Lobbyist", "Client"]

	write_to_csv("../Raw Data/unorganized_{}.csv".format(year), outputData, header)

def parse_1999():
	year = 1999
	filename = "../Raw Data/txts/1999-2000_WY_Lobbyist_List.txt"
	currentRow = 0
	lobbyistNameDelimiters = ["Lobbyist Name\n", "Lobbyist Name Address\n"]

	with open(filename) as txtFile:
		reader = txtFile.readlines()

	outputData = []
	currentLobbyName = ""

	while currentRow < len(reader):
		row = reader[currentRow]
		if "Lobbyist Name" in row:
			if "City, State, Zip" in reader[currentRow+1]:
				row = reader[currentRow+2]
			elif row not in lobbyistNameDelimiters:
				row = reader[currentRow]
			else:
				row = reader[currentRow+1]
			currentLobbyName = row.replace("\n", "")
		elif "Organization Information" in row:
			if "Address, City, State and Zip" in reader[currentRow+1]:
				row = reader[currentRow+3]
			else:
				row = reader[currentRow+1]
			outputData.append([currentLobbyName, row.replace("\n", "")])
		currentRow += 1

	header = ["Lobbyist", "Client"]

	write_to_csv("../Raw Data/unorganized_{}.csv".format(year), outputData, header)

def parse_2000():
	year = 2000
	filename = "../Raw Data/txts/2000-2001_WY_Lobbyist_List.txt"
	currentRow = 0
	lobbyistNameDelimiters = ["Lobbyist Name\n", "Lobbyist Name Address\n"]

	with open(filename) as txtFile:
		reader = txtFile.readlines()

	outputData = []
	currentLobbyName = ""

	while currentRow < len(reader):
		row = reader[currentRow]
		if "Lobbyist Name" in row:
			if "Address" in reader[currentRow+1]:
				row = reader[currentRow+4]
			elif row not in lobbyistNameDelimiters:
				row = reader[currentRow]
			else:
				row = reader[currentRow+1]
			currentLobbyName = row.replace("\n", "")
		elif "Organization Information" in row:
			if "Address, City, State and Zip" in reader[currentRow+1]:
				row = reader[currentRow+3]
			else:
				row = reader[currentRow+1]
			outputData.append([currentLobbyName, row.replace("\n", "")])
		currentRow += 1

	header = ["Lobbyist", "Client"]

	write_to_csv("../Raw Data/unorganized_{}.csv".format(year), outputData, header)

# Years, 2001, 2002, 2003
def parse_1():
	year = 2003
	filename = "../Raw Data/txts/2003-2004_WY_Lobbyist_List.txt"
	currentRow = 0
	lobbyistNameDelimiters = ["Lobbyist Name\n", "Lobbyist Name Address\n"]

	with open(filename) as txtFile:
		reader = txtFile.readlines()

	outputData = []
	currentLobbyName = ""

	while currentRow < len(reader):
		row = reader[currentRow]
		if "Lobbyist Name" in row:
			if "Address" in reader[currentRow+1]:
				if "E-mail Address" in reader[currentRow+3] or "E-Mail Address" in reader[currentRow+3] or "E-mail" in reader[currentRow+3] or "E-Mail" in reader[currentRow+3]:
					row = reader[currentRow+5]
				else:
					row = reader[currentRow+4]
			elif row not in lobbyistNameDelimiters:
				row = reader[currentRow]
			else:
				row = reader[currentRow+1]
			currentLobbyName = row.replace("\n", "")
		elif "Organization Information" in row:
			if "Address, City, State and Zip" in reader[currentRow+1]:
				row = reader[currentRow+2]
			else:
				row = reader[currentRow+1]
			outputData.append([currentLobbyName, row.replace("\n", "")])
		currentRow += 1

	header = ["Lobbyist", "Client"]

	write_to_csv("../Raw Data/unorganized_{}.csv".format(year), outputData, header)

# Years 2004
def parse_2():
	year = 2004
	filename = "../Raw Data/txts/2004-2005_WY_Lobbyist_List.txt"
	currentRow = 0
	lobbyistNameDelimiters = ["Lobbyist Name\n", "Lobbyist Name Address\n"]

	with open(filename) as txtFile:
		reader = txtFile.readlines()

	outputData = []
	currentLobbyName = ""

	while currentRow < len(reader):
		row = reader[currentRow]
		if "Lobbyist Name" in row:
			currentRow += 1
			while reader[currentRow] != "\n":
				currentRow += 1
				row = reader[currentRow+1]
			currentLobbyName = row.replace("\n", "")
		elif "Address, City, State and Zip" in row:
			row = reader[currentRow+2]
			outputData.append([currentLobbyName, row.replace("\n", "")])
		currentRow += 1

	header = ["Lobbyist", "Client"]

	write_to_csv("../Raw Data/unorganized_{}.csv".format(year), outputData, header)

# Years, 2005, 2006, 2007, 2008, 2009, 2010, 2011, 2012, 2013
def parse_3():
	year = 2013
	filename = "../Raw Data/txts/2013-2014_WY_Lobbyist_List.txt"
	currentRow = 0
	lobbyistNameDelimiters = ["Lobbyist Name\n", "Lobbyist Name Address\n"]

	with open(filename) as txtFile:
		reader = txtFile.readlines()

	outputData = []
	currentLobbyName = ""

	while currentRow < len(reader):
		row = reader[currentRow]
		if "Lobbyist" in row:
			if "Information" in reader[currentRow+1]:
				if "\n" == reader[currentRow+2]:
					if "Phone" in reader[currentRow+3]:
						currentRow += 3
						while reader[currentRow] != "\n":
							currentRow += 1
						row = reader[currentRow+1]
					else:
						row = reader[currentRow+3]
			currentLobbyName = row.replace("\n", "")
		elif "Organization Address" in row:
			if "\n" == reader[currentRow+1]:
				row = reader[currentRow+2]
			elif "\n" == reader[currentRow+3]:
				row = reader[currentRow+4]
			elif "\n" == reader[currentRow+4]:
				row = reader[currentRow+5]
			currentLobbyName = row.replace("\n", "")
		elif "Organization Information" in row:
			if "Address, City, State and Zip" in reader[currentRow+2]:
				row = reader[currentRow+4]
			else:
				row = reader[currentRow+1]
			outputData.append([currentLobbyName, row.replace("\n", "")])
		currentRow += 1

	header = ["Lobbyist", "Client"]

	write_to_csv("../Raw Data/unorganized_{}.csv".format(year), outputData, header)

# Years, 2014
def parse_4():
	year = 2014
	filename = "../Raw Data/txts/2014-2015_WY_Lobbyist_List.txt"
	currentRow = 0
	lobbyistNameDelimiters = ["Lobbyist Name\n", "Lobbyist Name Address\n"]

	with open(filename) as txtFile:
		reader = txtFile.readlines()

	outputData = []
	currentLobbyName = ""

	while currentRow < len(reader):
		row = reader[currentRow]
		if "Lobbyist" in row:
			if "Information" in reader[currentRow+1]:
				if "\n" == reader[currentRow+2]:
					if "Phone" in reader[currentRow+3]:
						currentRow += 3
						while reader[currentRow] != "\n":
							currentRow += 1
						row = reader[currentRow+1]
					else:
						row = reader[currentRow+3]
			currentLobbyName = row.replace("\n", "")
		elif "Organization Address" in row:
			if "\n" == reader[currentRow+1]:
				row = reader[currentRow+2]
			elif "\n" == reader[currentRow+3]:
				row = reader[currentRow+4]
			elif "\n" == reader[currentRow+4]:
				row = reader[currentRow+5]
			currentLobbyName = row.replace("\n", "")
		elif "Organization Information" in row:
			if "Address, City, State and Zip" in reader[currentRow+2]:
				row = reader[currentRow+4]
			else:
				row = reader[currentRow+1]
			outputData.append([currentLobbyName, row.replace("\n", "")])
		currentRow += 1

	header = ["Lobbyist", "Client"]

	write_to_csv("../Raw Data/unorganized_{}.csv".format(year), outputData, header)

if __name__ == "__main__":
	#parse_1998()
	#parse_1999()
	#parse_2000()
	#parse_1()
	#parse_2()			
	#parse_3()
	#parse_4()