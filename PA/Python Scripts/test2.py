from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time

if __name__ == "__main__":
	driver = webdriver.Chrome()
	driver.get('https://www.palobbyingservices.state.pa.us/Public/wfSearch.aspx')
	x = driver.find_elements_by_css_selector("#rblSearchType > tbody > tr > td:nth-child(2) > label")[0].click()
	x = driver.find_elements_by_css_selector("#rblRegistrationType > label:nth-child(4)")[0].click()
	search = driver.find_elements_by_css_selector("#btnQSearch")[0].click()
	time.sleep(20)
	nextP = driver.find_elements_by_css_selector("#MainContent_tcSearch_tpQuickSearch_ucQuickSearch_ui_Paging_ui_btnNext")[0].click()


	#rblSearchType > tbody > tr > td:nth-child(2) > label
	'''
	assert "Python" in driver.title
	elem = driver.find_element_by_name("q")
	elem.clear()
	elem.send_keys("pycon")
	elem.send_keys(Keys.RETURN)
	assert "No results found." not in driver.page_source
	'''
	time.sleep(20)
	driver.close()