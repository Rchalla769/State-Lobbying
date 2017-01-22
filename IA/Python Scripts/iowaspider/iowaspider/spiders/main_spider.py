#Author: Rohan Challa
#Email: rchalla@stanford.edu
#Date: October 14, 2016

import scrapy
from os import path
import os
import re
import csv

class MainSpider(scrapy.Spider):
	name = "main"
	labels = []
	data = []

	def start_requests(self):
		url = 'http://coolice.legis.iowa.gov/Cool-ICE/default.asp?Category=billinfo&Service=ClientReport&year='

		#years = ["2010", "2011", "2012", "2013", "2014", "2015", "2016"]
		years = ["2010"]

		for year in years:
			global filename 
			filename = ("IA_"+year+".csv")
			#try statement to remove previous file before writing new file
			try:
				os.remove(filename)
			except OSError:
				pass
			current_year = year

			yield scrapy.Request(url=(url+year), callback=self.parse)


	def parse(self, response):
		table_entries = response.css("table")[-1].css("a::text").extract()
		link_entries = response.css("table")[-1].css("a::attr(href)").extract()
		
		for link in link_entries:
			yield scrapy.Request(url=link, callback=self.parse_link)


	def parse_link(self, response):
		tag_entries = response.css("input").extract()
		value_entries = response.css("input::attr(value)").extract()
		name_entries = response.css("input::attr(name)").extract()

		print(name_entries)

		row = []

		for value in value_entries:
			row.append(value)

		with open(filename, 'a') as outcsv:
			#Specialized writer object to write to a csv file
			writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			writer.writerow(row)
		outcsv.close()