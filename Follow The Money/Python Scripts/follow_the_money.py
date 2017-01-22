#Author: Rohan Challa
#Email: rchalla@stanford.edu
#Date: October 09, 2016

from os import path
import os
import re
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
		writer.writerow(['State', 'Year', 'Name', 'Active', 'Industry', 'Number of Lobbyists'])
		for row in data:
			writer.writerow(row)
	outcsv.close()


if __name__ == '__main__':

	#Excluded files in the directory, might need to add more depending if there are other random folders
	excluded_files = [".DS_Store", "Python Scripts"]

	#Regular Expression to remove all html tags
	cleanr =re.compile('<.*?>')

	all_clients = []

	for directory in os.listdir("../"):
		if directory not in excluded_files:

			clients = []

			for file in os.listdir("../"+directory):
				if file not in excluded_files:
					if ".csv" not in file:

						print("directory: "+directory+"\tfile: "+file)

						with open("../"+directory+"/"+file) as f:
							content = f.readlines()
							found = []
							for line in content:
								if "<div role" in line:
									found.append(line)
		
							clients_mashed = found[-1]

							clients_split = clients_mashed.split("<tr")[2:]

							for client in clients_split:
								
								#cleans up the string and substitutes based on the regular expression
								cleantext = re.sub(cleanr,'*', client)
								cleantext = cleantext.replace("amp;", "")
								cleantext = cleantext[2:]
								client_list = list(filter(None, cleantext.split("*")))

								if len(client_list) == 5:
									client_list.insert(4, "")

								clients.append(client_list)
								all_clients.append(client_list)
						f.close()

			write_to_csv("../"+directory+"/"+directory+".csv", clients)
	write_to_csv("../Follow The Money.csv", all_clients)