#http://coolice.legis.iowa.gov/secure/default.asp?Category=ISLS1201&Service=CReportPrint&ReportNum=000926&year=2016

import scrapy

class LinkSpider(scrapy.Spider):
	name = "link"

	def start_requests(self):
		urls = [ 
			'http://coolice.legis.iowa.gov/secure/default.asp?Category=ISLS1201&Service=CReportPrint&ReportNum=000926&year=2016'
		]

		for url in urls:
			yield scrapy.Request(url=url, callback=self.parse)

	def parse(self, response):
		tag_entries = response.css("input").extract()
		value_entries = response.css("input::attr(value)").extract()
		name_entries = response.css("input::attr(name)").extract()
		
		for i in range(0, len(name_entries)):
			print("value: ", value_entries[i], "\tname: ", name_entries[i])
		