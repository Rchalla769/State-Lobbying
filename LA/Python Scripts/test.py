import requests
from bs4 import BeautifulSoup

if __name__ == "__main__":
	baseUrl = 'http://ethics.la.gov/LobbyistData/ResultsByLobbyistForm.aspx?SearchParams=ShowAll&OrderBy=1'
	currentSession = requests.Session()
	response = currentSession.get(baseUrl)
	soup = BeautifulSoup(response.content, 'lxml')
	#print(soup.prettify())

	viewState = soup.find("input", {"id":"__VIEWSTATE"}).get("value")
	previousPage = soup.find("input", {"id":"__PREVIOUSPAGE"}).get("value")
	eventValidation = soup.find("input", {"id":"__EVENTVALIDATION"}).get("value")

	table = soup.find("table", {'id':'ctl00_ContentPlaceHolder1_LobbyistGridView'})
	links = table.find_all('a')
	ids = []
	for link in links:
		idVal = link.get('id')
		if idVal and 'LobbyistGridView' in idVal:
			ids.append(idVal)

	formData = {'__EVENTTARGET': ids[0], '__VIEWSTATE': viewState, '__PREVIOUSPAGE': previousPage, '__EVENTVALIDATION': eventValidation, '__VIEWSTATEENCRYPTED':'', '__EVENTARGUMENT':'', '__LASTFOCUS':'', 'ctl00$ContentPlaceHolder1$LobbyistGridView$ctl01$GotoPageTextBox': 1}

	response = currentSession.post(baseUrl, formData)
	soup = BeautifulSoup(response.content, 'lxml')
	#print(soup.prettify())

	url = 'http://ethics.la.gov/LobbyistData/LobbyistDetail.aspx'
	response2 = currentSession.get(url)
	soup = BeautifulSoup(response2.content, 'lxml')
	print(soup.prettify())