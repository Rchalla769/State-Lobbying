from bs4 import BeautifulSoup
import csv
from os import path
import os
import scrapy
from scrapy.http import Request, FormRequest
import string

class NebraskaSpider(scrapy.Spider):
	name = "main"
	baseUrl = 'http://nebraskalegislature.gov/lobbyist/'
	outputFile = 'raw_data.csv'
	
	def start_requests(self):
		list_range = [1]
		list_range += list(string.ascii_uppercase)

		#try statement to remove previous file before writing new file
		try:
			os.remove(self.outputFile)
		except OSError:
			pass

		for listVal in list_range:
			url = "{}view.php?v=principal&list={}".format(self.baseUrl, listVal)
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		links = response.xpath('//table[@class="table table-condensed"]//a/@href').extract()
		for link in links:
			url = "{}{}".format(self.baseUrl, link)
			yield scrapy.Request(url=url, callback=self.parse_client_pages, meta={'url':url})

	def parse_client_pages(self, response):
		years = response.xpath('//select[@name="Year"]//option/text()').extract()[1:]
		for year in years:
			yield FormRequest(response.meta.get('url'), formdata={'Year':year}, callback=self.parse_year_pages, dont_filter=True, meta={'year':year})

	def parse_year_pages(self, response):
		clientName = response.xpath('//span[@id="PrincipalName"]/text()').extract_first()
		all_hrefs = response.xpath('//a[@class="list-group-item"]/@href').extract()

		for href in all_hrefs:
			if 'formc' in href:
				url = "{}{}".format(self.baseUrl, href)
				yield Request(url, callback=self.parse_page, meta={'year':response.meta.get('year'), 'client': clientName})

	def parse_page(self, response):
		lobbyists = response.xpath('//p[@id="Lobbyists"]/text()').extract_first().replace('\n', '').strip()
		amount = float(response.xpath('//p[@id="TotalExpenses"]/text()').extract_first().replace(',', ''))

		row = ["Nebraska", "NE", response.meta.get('year'), response.meta.get('client'), amount, lobbyists]

		with open(self.outputFile, 'a') as outcsv:
			writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			writer.writerow(row)
		outcsv.close()



