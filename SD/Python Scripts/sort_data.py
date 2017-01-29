from os import path
import os
import csv

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
	filename = "./spider/raw_data.csv"

	with open(filename) as f:
		reader = csv.reader(f)
		data = {}
		for row in reader:
			year = row[0]
			client = row[1]
			amount = float(row[3])
			lobbyist = row[2]

			if year in data:
				if client in data[year]:
					data[year][client]["amount"] += amount
					if lobbyist not in data[year][client]["lobbyists"]:
						data[year][client]["lobbyists"].append(lobbyist)
				else:
					data[year][client] = {"amount": amount, "lobbyists": [lobbyist]}
			else:
				data[year] = {client: {'lobbyists':[lobbyist], 'amount': amount}}

	for (year, clients) in data.items():
		rows = []
		for (client, info) in clients.items():
			row = ["South Dakota", "SD", year, client, info["amount"]]
			row += info["lobbyists"]
			rows.append(row)
		write_to_csv("../SD_{}.csv".format(year), rows)
		print("{} finished!!".format(year))
	print("ALL DONE!!")