from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
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
		#writer.writerow(['State', 'StateAbbr', 'Year', 'Client', 'Amount', 'Lobbyist1', 'Lobbyist2', 'Lobbyist3', 'Lobbyist4', 'Lobbyist5', 'Lobbyist6', 'Lobbyist7', 'Lobbyist8', 'Lobbyist9', 'Lobbyist10', 'Lobbyist11', 'Lobbyist12'])
		for row in data:
			writer.writerow(row)
	outcsv.close()

if __name__ == "__main__":
	# Base URL: https://apps.tn.gov/ilobbysearch-app/viewEmployerDashboard.htm?employerId=365
	# Need to test to see how many employerIds there are and change accordingly
	numberOfClients = 1840

	data = []

	driver = webdriver.Chrome()
	driver.get("https://apps.tn.gov/ilobbysearch-app/search.htm")
	for i in range(0, numberOfClients+1):
		driver.get("https://apps.tn.gov/ilobbysearch-app/viewEmployerDashboard.htm?employerId={}".format(i))
		hrefs = []
		dates = []
		lobbyists = []
		
		x = driver.find_elements_by_css_selector("a[href*='reportId']")
		if len(x) > 0:
			
			for i in x:
				dates.append(i.text)
				hrefs.append(i.get_attribute("href"))
				#print("{}\n{}\n".format(i.text, i.get_attribute("href")))
		

		y = driver.find_elements_by_css_selector("a[href*='lobbyistId']")
		if len(y) > 0:
			for i in y:
				lobbyists.append(i.text)
				#print(i.text)
		#print()

		row = []
		for i in range(0, len(hrefs)):
			row.append("Date")
			row.append(dates[i])

			driver.get(hrefs[i])

			all_ps = driver.find_elements_by_tag_name("p")
			for p in all_ps:
				#print(p.text)
				row.append(p.text)

			row.append("Lobbyists")
			for lobby in lobbyists:
				row.append(lobby)

			data.append(row)
			row = []

	time.sleep(3)
	driver.close()

	write_to_csv("Raw_Data.csv", data)
	print("DONE")