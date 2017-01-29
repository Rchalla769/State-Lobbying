from bs4 import BeautifulSoup
import csv
from os import path
import os
import scrapy
from scrapy.http import Request, FormRequest
import string

class SouthDakotaSpider(scrapy.Spider):
	name = "main"
	baseUrl = 'https://sos.sd.gov/Lobbyist/LRPublicAccess.aspx'
	outputFile = 'raw_data.csv'
	max_page = 7

	def reverse_name(self, name):
		names = name.split(', ')
		return '{} {}'.format(names[1], names[0])

	def strip_dollars(self, dollar):
		dollar = dollar.replace('$', '')
		dollar = dollar.replace(',', '')
		return dollar
	
	def start_requests(self):
		#try statement to remove previous file before writing new file
		try:
			os.remove(self.outputFile)
		except OSError:
			pass

		yield scrapy.Request(url=self.baseUrl, callback=self.parse)

	def parse(self, response):
		viewState = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
		viewStateGenerator = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
		eventValidation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first()

		formData = {
		'ctl00_RadScriptManager1_TSM':';;System.Web.Extensions, Version=4.0.0.0, Culture=neutral, PublicKeyToken=31bf3856ad364e35:en-US:4bd8faf8-554d-46be-b2ff-c9d57adb612c:ea597d4b:b25378d2;Telerik.Web.UI, Version=2014.1.403.40, Culture=neutral, PublicKeyToken=121fae78165ba3d4:en-US:ca584452-327f-4858-bf00-fb22c6f6fd75:16e4e7cd:f7645509:ed16cbdc:88144a7a:24ee1bba:7165f74:e330518b:1e771326:8e6f0d33:6a6d718d:f46195d3:2003d0b8:aa288e2d:258f1c72:b7778d6c:58366029',
		'__EVENTTARGET': '',
		'__EVENTARGUMENT': '',
		'__VIEWSTATE': viewState,
		'__VIEWSTATEGENERATOR': viewStateGenerator,
		'__EVENTVALIDATION': eventValidation,
		'ctl00_MainContent_btnHomepge_ClientState':'',
		'ctl00_MainContent_RadTabStripSearchOptions_ClientState':'{"selectedIndexes":["0"],"logEntries":[],"scrollState":{}}',
		'ctl00$MainContent$cboSessionsPriSearch':'All Years',
		'ctl00_MainContent_cboSessionsPriSearch_ClientState':'',
		'ctl00$MainContent$txtWordSearch':'Enter a Word to Search for',
		'ctl00_MainContent_txtWordSearch_ClientState':'{"enabled":true,"emptyMessage":"Enter a Word to Search for","validationText":"","valueAsString":"","lastSetTextBoxValue":"Enter a Word to Search for"}',
		'ctl00$MainContent$cboWordSearchType':'Wildcard-Default: This finds all words or partial words that match what you entered.',
		'ctl00_MainContent_cboWordSearchType_ClientState':'',
		'ctl00$MainContent$btnPriSearch':'Go',
		'ctl00_MainContent_radGrdPriSearchResults_ClientState':'',
		'ctl00$MainContent$cboSessionsPrivatePrint':'2017',
		'ctl00_MainContent_cboSessionsPrivatePrint_ClientState':'',
		'ctl00$MainContent$cboSessionsPubSearch':'All Years',
		'ctl00_MainContent_cboSessionsPubSearch_ClientState':'',
		'ctl00_MainContent_radgrdPublic_ClientState':'',
		'ctl00$MainContent$cboSessionsPublicPrint':'2017',
		'ctl00_MainContent_cboSessionsPublicPrint_ClientState':'',
		'ctl00_MainContent_RadMultiPageSearchType_ClientState':'',
		'ctl00$MainContent$hdfpreviousTab':'' 
		}
		url = 'https://sos.sd.gov/Lobbyist/LRPublicAccess.aspx'
		yield FormRequest(url, formdata=formData, callback=self.parse_pages, dont_filter=True, meta={'formData': formData, 'i':0})

	def parse_pages(self, response):
		if response.meta.get('i') != self.max_page:
			formData = response.meta.get('formData')

			div = response.xpath('//div[@class="RadGrid RadGrid_Default"]')
			links = div[0].xpath('//a[contains(@href, "LRRptLobbyist")]/@href').extract()
			names = div[0].xpath('//a[contains(@href, "LRRptLobbyist")]//text()').extract()

			for i in range(0, len(links)):
				url = '{}{}'.format('https://sos.sd.gov/Lobbyist/', links[i])
				yield scrapy.Request(url=url, callback=self.parse_company_page, dont_filter=True, meta={'name':self.reverse_name(names[i])})

			viewState = response.xpath('//input[@id="__VIEWSTATE"]/@value').extract_first()
			viewStateGenerator = response.xpath('//input[@id="__VIEWSTATEGENERATOR"]/@value').extract_first()
			eventValidation = response.xpath('//input[@id="__EVENTVALIDATION"]/@value').extract_first()

			if 'ctl00$MainContent$btnPriSearch' in formData:
				del formData['ctl00$MainContent$btnPriSearch']
			formData['ctl00$MainContent$radGrdPriSearchResults$ctl00$ctl03$ctl01$ctl22'] = '' 
			formData['ctl00$MainContent$radGrdPriSearchResults$ctl00$ctl03$ctl01$PageSizeComboBox'] = '500'
			formData['ctl00_MainContent_radGrdPriSearchResults_ctl00_ctl03_ctl01_PageSizeComboBox_ClientState'] = ''
			formData['__VIEWSTATE'] = viewState
			formData['__VIEWSTATEGENERATOR'] = viewStateGenerator
			formData['__EVENTVALIDATION'] = eventValidation

			url = 'https://sos.sd.gov/Lobbyist/LRPublicAccess.aspx'
			yield FormRequest(url, formdata=formData, callback=self.parse_pages, dont_filter=True, meta={'formData': formData, 'i':(response.meta.get('i')+1)})

	def parse_company_page(self, response):
		year = response.xpath('//input[@id="ctl00_MainContent_txtLegSession"]/@value').extract_first()
		if year is None:
			year = 2019

		name = response.meta.get('name')
		clients = response.xpath('//tr[contains(@id, "grEmployerInfo")]//td/text()').extract()
		
		for i in range(0, len(clients), 4):
			self.write_to_csv(name, year, clients[i], 0)

		clients = response.xpath('//tr[contains(@id, "grExpenses")]//td/text()').extract()

		for i in range(0, len(clients), 7):
			self.write_to_csv(name, year, clients[i], self.strip_dollars(clients[i+6]))

	def write_to_csv(self, name, year, client, amount):
		row = [year, client, name, amount]
		with open(self.outputFile, 'a') as outcsv:
			writer = csv.writer(outcsv, delimiter=',', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
			writer.writerow(row)
		outcsv.close()