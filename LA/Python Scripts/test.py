import requests
from bs4 import BeautifulSoup

def reverse_name(name):
	names = name.split(', ')
	return "{} {}".format(names[1], names[0])

if __name__ == "__main__":
	baseUrl = 'http://ethics.la.gov/LobbyistData/ResultsByLobbyistForm.aspx?SearchParams=ShowAll&OrderBy=1'
	currentSession = requests.Session()
	response = currentSession.get(baseUrl)
	soup = BeautifulSoup(response.content, 'lxml')
	#print(soup.prettify())

	table = soup.find("table", {'id':'ctl00_ContentPlaceHolder1_LobbyistGridView'})
	links = table.find_all('a')
	ids = []
	names = []
	for link in links:
		idVal = link.get('id')
		if idVal and 'LobbyistGridView' in idVal:
			ids.append(idVal.replace('_', '$'))
			names.append(reverse_name(link.get_text()))

	print(ids)

	viewState = soup.find("input", {"id":"__VIEWSTATE"}).get("value")
	previousPage = soup.find("input", {"id":"__PREVIOUSPAGE"}).get("value")
	eventValidation = soup.find("input", {"id":"__EVENTVALIDATION"}).get("value")

	formData = {'__VIEWSTATE': viewState, '__PREVIOUSPAGE': previousPage, '__EVENTVALIDATION': eventValidation, '__VIEWSTATEENCRYPTED':'', '__EVENTARGUMENT':'', '__LASTFOCUS':'', 'ctl00$ContentPlaceHolder1$LobbyistGridView$ctl01$GotoPageTextBox': '1', 'ctl00$ContentPlaceHolder1$LobbyistGridView$ctl01$NextLinkButton':'Next'}

	response = currentSession.post(baseUrl, formData)
	soup = BeautifulSoup(response.content, 'lxml')

	table = soup.find("table", {'id':'ctl00_ContentPlaceHolder1_LobbyistGridView'})
	links = table.find_all('a')
	ids = []
	names = []
	for link in links:
		idVal = link.get('id')
		if idVal and 'LobbyistGridView' in idVal:
			ids.append(idVal.replace('_', '$'))
			names.append(reverse_name(link.get_text()))

	print(names)

