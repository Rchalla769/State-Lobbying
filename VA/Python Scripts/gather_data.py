from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException
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
		writer.writerow(['State', 'StateAbbr', 'Year', 'Client', 'Amount', 'Lobbyist1', 'Lobbyist2', 'Lobbyist3', 'Lobbyist4', 'Lobbyist5', 'Lobbyist6', 'Lobbyist7', 'Lobbyist8', 'Lobbyist9', 'Lobbyist10', 'Lobbyist11', 'Lobbyist12'])
		for row in data:
			writer.writerow(row)
	outcsv.close()

def strip_money(value):
	value = value.replace("$", "")
	value = value.replace(",", "")
	value = value.replace(" ", "")
	return float(value)

if __name__ == "__main__":
	data = []

	driver = webdriver.Chrome()
	driver.get("https://solutions.virginia.gov/Lobbyist/Reports/DisclosureSearch")

	searchButton = driver.find_element_by_id("Submit1")

	year = driver.find_element_by_id('registrationYear')
	yearOptions = year.find_elements_by_tag_name('option')

	name = driver.find_element_by_id('principal')
	companyOptions = name.find_elements_by_tag_name('option')

	yearOptions[0].click()
	searchButton.click()

	for i in range(0, len(yearOptions)):
		year = driver.find_element_by_id('registrationYear')
		yearOptions = year.find_elements_by_tag_name('option')
		yearOptions[i].click()

		year = yearOptions[i].text.split(" - ")[0]
		yearData = []

		for j in range(0, len(companyOptions)):
			searchButton = driver.find_element_by_id("Submit1")

			name = driver.find_element_by_id('principal')
			companyOptions = name.find_elements_by_tag_name('option')
			companyName = companyOptions[j].text
			companyOptions[j].click()

			searchButton.click()

			lobby = driver.find_element_by_css_selector("#lobbyistList > tbody > tr > td")
			if lobby.text != "No data available in table":
				lobbyTable = driver.find_element_by_css_selector("#lobbyistList > tbody")
				sum = 0
				lobbyists = []
				odd = lobbyTable.find_elements_by_class_name("odd")
				for temp in odd:
					try:
						lobbyName = temp.find_element_by_css_selector("td.sorting_1 > a")
						lobbyists.append(lobbyName.text)
					except NoSuchElementException:
						x = 0
					try:
						extra = temp.find_element_by_css_selector("td:nth-child(4)")
						sum += strip_money(extra.text)
					except NoSuchElementException:
						x = 0
					

				even = lobbyTable.find_elements_by_class_name("even")
				for temp in even:
					try:
						lobbyName = temp.find_element_by_css_selector("td.sorting_1 > a")
						lobbyists.append(lobbyName.text)
					except NoSuchElementException:
						x = 0

					try:
						extra = temp.find_element_by_css_selector("td:nth-child(4)")
						sum += strip_money(extra.text)
					except NoSuchElementException:
						x = 0

				row = ["Virginia", "VA", year, companyName, sum]

				for lobbyist in lobbyists:
					row.append(lobbyist)
				print(row)
				yearData.append(row)
	write_to_csv("../Raw Data/{}.csv".format(year), yearData)
	print("{} finished!".format(year))

time.sleep(2)
driver.close()
print("DONE")