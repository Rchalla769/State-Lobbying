import requests
import json
import pprint
from bs4 import BeautifulSoup
import csv
from os import path
import os

def clean_values(value):
	value = value.replace("\n", "")
	if "$" in value:
		value = value.replace("$", "")
		value = value.replace(",", "")
	return value

def pull_useful_data(parentDiv):
	totalData = []
	sections = parentDiv.find_all("tr")
	for section in sections:
		if section.has_attr('class'):
			data = []
			tds = section.find_all("td")
			for i in range(1, len(tds)):
				data.append(clean_values(tds[i].text))
			if len(data) != 0:
				totalData.append(data)
	return totalData

if __name__ == "__main__":
	baseUrl = 'https://www.palobbyingservices.state.pa.us/Public/wfSearch.aspx'
	currentSession = requests.Session()
	response = currentSession.get(baseUrl)
	soup = BeautifulSoup(response.content, 'lxml')

	toolkitScript = ';;AjaxControlToolkit, Version=3.5.40412.0, Culture=neutral, PublicKeyToken=28f01b0e84b6d53e:en-US:1547e793-5b7e-48fe-8490-03a375b13a33:de1feab2:f9cec9bc:a0b0f951:a67c2700:f2c8e708:720a52bf:4a2c8239'
	mainContent = '{"ActiveTabIndex":0,"TabState":[true,true,true]}'
	viewState = soup.find("input", {"id":"__VIEWSTATE"}).get("value")
	viewStateGenerator = soup.find("input", {"id":"__VIEWSTATEGENERATOR"}).get("value")
	previousPage = soup.find("input", {"id":"__PREVIOUSPAGE"}).get("value")
	eventValidation = soup.find("input", {"id":"__EVENTVALIDATION"}).get("value")

	formData = {'ToolkitScriptManager1_HiddenField':toolkitScript,
				'MainContent_tcSearch_ClientState':mainContent,
				'__VIEWSTATE':viewState,
				'__VIEWSTATEGENERATOR':viewStateGenerator,
				'__VIEWSTATEENCRYPTED':'',
				'__PREVIOUSPAGE':previousPage,
				'__EVENTVALIDATION':eventValidation,
				'ctl00$ddlRegHelp':'-1',
				'ctl00$ddlTakeTour':'-1',
				'ctl00$ucLeftNav$hdnLastTab':'0',
				'ctl00$ucLeftNav$ucLoginControl$txtUserID':'',
				'ctl00$ucLeftNav$ucLoginControl$txtPassword':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$rblSearchType':'Expenses',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$rblRegistrationType':'P',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$hdtext':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtRegNumber':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtPrincipalName':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtFirmName':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtLFirstName':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtMiddleName':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtLLastName':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtSuffix':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$btnQSearch.x':'40',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$btnQSearch.y':'12',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtPACName':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtPACAcronym':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtPACRegNo':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ddlBusinessNature':'ALL',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ddlSearchLobbyingSubject':'ALL',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtDateFrom':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtDateTo':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ddlregPeriodID':'5',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ddlSearchYear':'0',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ddlSearchQuarter':'0',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtLine1':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtLine2':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtCity':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ddlSearchState':'PA',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtZipCode':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$txtPlus4':'',
				'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$CollapsiblePanelExtender1_ClientState':'true',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl00$HiddenField1':'4',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl00$hdnYear':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl00$hdnQuarter':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl00$ddlPaymentExpenseYear':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl00$ddlPaymentExpenseQuarter':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl01$HiddenField1':'2',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl01$hdnYear':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl01$hdnQuarter':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl01$ddlPaymentExpenseYear':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl01$ddlPaymentExpenseQuarter':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl02$HiddenField1':'1',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl02$hdnYear':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl02$hdnQuarter':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl02$ddlPaymentExpenseYear':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl02$ddlPaymentExpenseQuarter':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl03$HiddenField1':'3',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl03$hdnYear':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl03$hdnQuarter':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl03$ddlPaymentExpenseYear':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl03$ddlPaymentExpenseQuarter':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl04$HiddenField1':'5',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl04$hdnYear':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl04$hdnQuarter':'True',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl04$ddlPaymentExpenseYear':'0',
				'ctl00$MainContent$tcSearch$tpPublicReport$ucPublicReports$ReportRepeater$ctl04$ddlPaymentExpenseQuarter':'0',
				'ctl00$MainContent$tcSearch$tpDirectory$ucDirectory$txtLastName':'',
				'ctl00$MainContent$tcSearch$tpDirectory$ucDirectory$txtFirstName':'',
				'ctl00$MainContent$tcSearch$tpDirectory$ucDirectory$txtMiddleName':'',
				'ctl00$MainContent$tcSearch$tpDirectory$ucDirectory$txtSuffix':'',
				'ctl00$hdnSelectedTab':'0' }

	url = 'https://www.palobbyingservices.state.pa.us/Public/wfSearch.aspx'
	response = currentSession.post(url, formData)
	soup = BeautifulSoup(response.content, 'lxml')
	parentDiv = soup.find("div", {"id":"divSearchResult"})
	totalData = pull_useful_data(parentDiv)
	print(totalData)


	viewState = soup.find("input", {"id":"__VIEWSTATE"}).get("value")
	formData['__VIEWSTATE'] = viewState
	previousPage = soup.find("input", {"id":"__PREVIOUSPAGE"}).get("value")
	formData['__PREVIOUSPAGE'] = previousPage
	eventValidation = soup.find("input", {"id":"__EVENTVALIDATION"}).get("value")
	formData['__EVENTVALIDATION'] = eventValidation
	nextPage = 'ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$UpdatePanel1|ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ui_Paging$ui_btnGo'
	formData["ctl00$ToolkitScriptManager1"] = nextPage
	formData['ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ui_Paging$ui_ddlGo'] = 2
	formData["__ASYNCPOST"] = "true"

	'''
	del formData['ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$btnQSearch.x']
	del formData['ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$btnQSearch.y']
	formData["__ASYNCPOST"] = "true"
	formData['ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ui_Paging$ui_btnNext.x'] = 34
	formData['ctl00$MainContent$tcSearch$tpQuickSearch$ucQuickSearch$ui_Paging$ui_btnNext.y'] = 5
	'''

	response = currentSession.post(url, formData)
	print(response.content)


	#soup = BeautifulSoup(response.content, 'lxml')
	#print(soup.prettify)