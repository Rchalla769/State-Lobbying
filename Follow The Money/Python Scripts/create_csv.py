#Author: Rohan Challa
#Email: rchalla@stanford.edu
#Date: OCtober 09, 2016

from os import path
import os
import re
import csv

if __name__ == '__main__':

	files = [
			"../Alabama/2006.html", "../Alabama/2007.html", "../Alabama/2008.html", 
			"../Alabama/2009.html", "../Alabama/2010.html", "../Alabama/2011.html", 
			"../Alabama/2012.html", "../Alabama/2013.html", "../Alabama/2014.html", 
			"../Alabama/2015.html"
			]
	filename = "../Alabama/Alabama.csv"

	try:
		os.remove(filename)
	except OSError:
		pass
		
	with open(filename, 'a') as outcsv:
		writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
		writer.writerow(['State', 'Year', 'Name', 'Active', 'Industry', 'Number of Lobbyists'])

		for file in files:
			with open(file) as f:
				content = f.readlines()
				count = 0
				found = []
				for line in content:
					if "<div role" in line:
						found.append(line)
						count += 1
		
				clients_mashed = found[-1]

				clients_split = clients_mashed.split("<tr")
				clients_split = clients_split[2:]

				cleanr =re.compile('<.*?>')
		

				for client in clients_split:
					cleantext = re.sub(cleanr,'*', client)
					cleantext = cleantext.replace("amp;", "")
					cleantext = cleantext[2:]
					x = list(filter(None, cleantext.split("*")))

					if len(x) == 5:
						x.insert(4, "")

					#configure writer to write standard csv file
					writer.writerow(x)
			f.close
	outcsv.close