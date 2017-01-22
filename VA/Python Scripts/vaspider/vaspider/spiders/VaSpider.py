import csv
from os import path
import os
import scrapy
from scrapy.contrib.spiders.init import InitSpider
from scrapy.http import Request, FormRequest
import logging

class VaSpider(InitSpider):
	# To run: go to top of project's directory and run scrapy crawl main
	name = "main"
	years = []
	yearIds = []
	companies = []
	companyIds = []

	def init_request(self):
		mainURL = "https://solutions.virginia.gov/Lobbyist/Reports/DisclosureSearch"
		formData = {"registrationYear":"315880000", "principal":"fbf94291-a6a1-4a7b-a95e-a958bc83fd9d"}

		logging.info("This is an info")

		return FormRequest(mainURL, formdata=formData, callback=self.start)

	def start(self, response):
		yearSelector = response.selector.xpath("//select[@id='registrationYear']").extract()
		print(yearSelector)
		'''
		selector = soup.find('select', id="registrationYear")
		for x in selector.find_all("option"):
			self.years.append(x.text)
			self.yearIds.append(x.get("value"))
	
		selector = soup.find('select', id="principal")
		for x in selector.find_all("option"):
			self.companies.append(x.text)
			self.companyIds.append(x.get("value"))
		'''
		return self.initialized()

	def start_requests(self):
		urls = [
		'http://quotes.toscrape.com/page/1/',
		'http://quotes.toscrape.com/page/2/',
		]
		for url in urls:
			yield Request(url=url, callback=self.parse)

	def parse(self, response):
		print(response)
