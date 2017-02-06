from bs4 import BeautifulSoup
import csv
from os import path
import os
import scrapy
from scrapy.http import Request, FormRequest
import string

class SouthDakotaSpider(scrapy.Spider):
	name = "main"
	baseUrl = 'http://ethics.la.gov/LobbyistData/ResultsByLobbyistForm.aspx?SearchParams=ShowAll&OrderBy=1'
	outputFile = 'raw_data.csv'
	max_page = 63

	def reverse_name(self, name):
		names = name.split(', ')
		return '{} {}'.format(names[1], names[0])

	def clean_amount(self, value):
		value = value.replace(',', '')
		value = value.replace('or less', '')
		value = value.replace('or more', '')
		value = value.replace('$', '')
		value = value.replace(' ', '')
		values = value.split('-')
		if len(values) > 1:
			s = float(values[0]) + float(values[1])
			return (s/2)
		else:
			return float(values[0])

	def clean_dates(self, val1, val2):
		if val2 == 'current':
			val2 = '1/1/2017'

		year1 = int(val1[-4:len(val1)])
		year2 = int(val2[-4:len(val2)])

		years = []
		for i in range(year1, year2+1):
			years.append(i)
		return years

	def start_requests(self):
		#try statement to remove previous file before writing new file
		try:
			os.remove(self.outputFile)
		except OSError:
			pass

		yield scrapy.Request(url=self.baseUrl, callback=self.parse, meta={'i':0})

	def parse(self, response):
		if response.meta.get('i') != self.max_page:
			links = response.xpath('//table[@id="ctl00_ContentPlaceHolder1_LobbyistGridView"]//a[contains(@href, "LobbyistGridView")]/@id').extract()
			names = response.xpath('//table[@id="ctl00_ContentPlaceHolder1_LobbyistGridView"]//a[contains(@href, "LobbyistGridView")]//span/text()').extract()

			links = [link.replace('_','$') for link in links]
			names = [self.reverse_name(name) for name in names]

			viewState = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
			previousPage = response.xpath('//input[@id="__PREVIOUSPAGE"]/@value').extract_first()
			eventValidation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first()

			for i in range(0, len(links)):
				formData = {'__EVENTTARGET': links[i], '__VIEWSTATE': viewState, '__PREVIOUSPAGE': previousPage, '__EVENTVALIDATION': eventValidation, '__VIEWSTATEENCRYPTED':'', '__EVENTARGUMENT':'', '__LASTFOCUS':'', 'ctl00$ContentPlaceHolder1$LobbyistGridView$ctl01$GotoPageTextBox':'1'}

				yield FormRequest(self.baseUrl, formdata=formData, callback=self.parse_pages, dont_filter=True, meta={'name':names[i]})

			formData = {'__VIEWSTATE': viewState, '__PREVIOUSPAGE': previousPage, '__EVENTVALIDATION': eventValidation, '__VIEWSTATEENCRYPTED':'', '__EVENTARGUMENT':'', '__LASTFOCUS':'', 'ctl00$ContentPlaceHolder1$LobbyistGridView$ctl01$GotoPageTextBox':str(response.meta.get('i')+1), 'ctl00$ContentPlaceHolder1$LobbyistGridView$ctl01$NextLinkButton':'Next'}
			yield FormRequest(url=self.baseUrl, formdata=formData, callback=self.parse, meta={'i':response.meta.get('i')+1})

	def parse_pages(self, response):
		tds = response.xpath('//table[@id="ctl00_ContentPlaceHolder1_CompRepGridView"]//td/text()').extract()
		spans = response.xpath('//table[@id="ctl00_ContentPlaceHolder1_CompRepGridView"]//span/text()').extract()
		td = []
		for t in tds:
			if '$' in t:
				td.append(t)

		if len(spans) % 4 != 0:
			spans = spans[0:len(spans)-1]

		for i in range(0, len(spans), 4):
			client = spans[i]
			years = self.clean_dates(spans[i+2], spans[i+3])
			if len(years) != 0:
				amount = (self.clean_amount(td[i//4]))/(len(years))
			else:
				amount = self.clean_amount(td[i//4])
			for year in years:
				self.write_to_csv(response.meta.get('name'), year, client, amount)

	def write_to_csv(self, name, year, client, amount):
		row = [year, client, name, amount]
		with open(self.outputFile, 'a') as outcsv:
			writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			writer.writerow(row)
		outcsv.close()