from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import time
import csv
import re

url_lists = ['https://www.zhihu.com/people/bei-li-kou-58/pins',
			 'https://www.zhihu.com/people/ye-bo-zs/pins']


def load_page(n, sleep=1):
	for _ in range(n):
		time.sleep(sleep)

		bts = browser.find_elements(By.XPATH, '//button[text()="阅读全文"]')
		for bt in bts:
			bt.click()

		browser.execute_script("window.scrollTo(0,document.body.scrollHeight)")

		bts = browser.find_elements(By.XPATH, '//button[text()="阅读全文"]')
		for bt in bts:
			bt.click()

def export_ideas(browser, url, sleep=1):
	browser.get(url)

	ideas = []
	votes = []
	urls = []
	times = []

	while True:
		load_page(1)

		soup=BeautifulSoup(browser.page_source,'lxml')

		for idea in soup.find_all("span", class_="RichText ztext CopyrightRichText-richText"):
			ideas.append(idea.get_text())

		for vote in soup.find_all("span", class_="Voters"):
			votes.append(re.findall(r'\b\d+\b', vote.get_text())[-1])

		for s in soup.find_all("div", class_="ContentItem-time"):
			urls.append(s.a['href'])
			times.append(s.span['data-tooltip'][4:])

		try:
			browser.find_element(By.XPATH, '//button[text()="下一页"]').click()
		except:
			break

	filename = browser.title

	with open(filename+'.csv', 'w', encoding='utf-8') as file:
	    wr = csv.writer(file)
	    wr.writerow(['idea','votes','url','time'])
	    for row in zip(ideas, votes, urls, times):
	    	wr.writerow(row)


if __name__ == '__main__':

	browser = webdriver.Chrome()
	browser.implicitly_wait(2)

	for url in url_lists:
		export_ideas(browser, url)

	browser.close()



