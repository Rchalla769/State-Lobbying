#Author: Rohan Challa
#Email: rchalla@stanford.edu
#Date: October 27, 2016

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

def get_year(date):
	date_split = date.split("/")
	return date_split[-1]

def create_dict(data):
	dictionary = {}
	for row in data:
		year = get_year(row[1])
		if year in dictionary:
			dictionary[year].append(row[2:])
		else:
			dictionary[year] = [row[2:]]
	return dictionary	

def row_to_dict(row):
	dictionary = {}
	for i in range(0, len(row)):
		splitElems = row[i].split("\n")
		if splitElems[0] == "Lobbyists":
			break

		if splitElems[0] in dictionary:
			dictionary[splitElems[0]].append(splitElems[-1])
		else:
			dictionary[splitElems[0]] = [splitElems[-1]]
	dictionary["Lobbyists"] = []
	for j in range(i+1, len(row)):
		dictionary["Lobbyists"].append(row[j])
	return dictionary

def remove_noise(data):
	clean_data = {}
	for key in data:
		clean_data[key] = []
		for row in data[key]:
			clean_data[key].append(row_to_dict(row))
	return clean_data

def clean_money(salary):
	if "$" in salary:
		salary = salary.replace("$","")
	if "," in salary:
		salary = salary.replace(",", "")
	return float(salary)

def get_amount(totals):
	sum = 0

	for total in totals:
		if total is None:
			sum += 0
		elif "Less than " in total:
			current = total[len("Less than "):]
			sum += clean_money(current)
		elif " - " in total:
			current = total.split(" - ")
			avg = (clean_money(current[0]) + clean_money(current[-1]))/2
			sum += avg
		elif "$" in total:
			sum += clean_money(total)

	return sum

def dict_to_row(data, year):
	newRow = []
	if "Name" in data:
		newRow.append("Tennessee")
		newRow.append("TN")
		newRow.append(year)
		newRow.append(data["Name"][0])
		newRow.append(get_amount(data["Total"]))
		newRow += data["Lobbyists"]
	return newRow

def find_similarities(data):
	toReturn = {}

	for key in data:
		toReturn[key] = []
		tempDict = {}
		for value in data[key]:
			name = value[3]
			if name in tempDict:
				amount = value[4]
				tempDict[name][4] += amount
			else:
				tempDict[name] = value
		toReturn[key] = tempDict

	newDict = {}
	for key in toReturn:
		newDict[key] = []
		for value in toReturn[key]:
			newDict[key].append(toReturn[key][value])

	return newDict
	#print(newDict)
		
if __name__ == '__main__':
	filename = "../Raw Data/Raw_Data.csv"
	with open(filename) as f:
		reader = csv.reader(f)
		array = []
		for row in reader:
			array.append(row)

		data = create_dict(array)
		data = remove_noise(data)

		final_data = {}

		for key in data:
			final_data[key] = []
			for dictionary in data[key]:
				newRow = dict_to_row(dictionary, key)
				if len(newRow) != 0:
					final_data[key].append(newRow)

		final_data = find_similarities(final_data)

		for key in final_data:
			write_to_csv("../TN_{}.csv".format(key), final_data[key])
