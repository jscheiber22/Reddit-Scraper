import undetected_chromedriver as uc
import multiprocessing as mp
import sys
import os
import subprocess
from time import sleep
import re


class Reddit:
	def __init__(self):
		chrome_options = uc.ChromeOptions()
		chrome_options.add_argument("--disable-blink-features")
		chrome_options.add_argument("--disable-blink-features=AutomationControlled")
		# chrome_options.add_argument("--headless")
		self.driver = uc.Chrome(options=chrome_options)

	def getLinks(self):
		links = []

		self.driver.get('https://www.reddit.com/r/wallstreetbets/')
		sleep(3)
		self.driver.get('https://www.reddit.com/r/wallstreetbets/')
		sleep(3)

		images = self.driver.find_elements_by_xpath('//img')
		for image in images:
			src = image.get_attribute('src')
			if 'preview' in src and not 'award_images' in src:
				title = image.find_element_by_xpath('./../../..').get_attribute('href')
				title = re.search('/comments/.*/.*/', title)
				if title is not None:
					title = title.group().replace('/comments/', '')
					title = re.search('/.*/', title)
					if title is not None:
						links.append(title.group() + '...' + src)

		if len(links) > 0:
			return links
		else:
			print('Pulled no links :/')
			self.driver.close()

	def scroll_down(self):
		"""A method for scrolling the page."""

		# Get scroll height.
		last_height = self.driver.execute_script("return document.body.scrollHeight")

		while True:

			# Scroll down to the bottom.
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			# Wait to load the page.
			time.sleep(2)

			# Calculate new scroll height and compare with last scroll height.
			new_height = self.driver.execute_script("return document.body.scrollHeight")

			if new_height == last_height:

				break

			last_height = new_height


def curlLinks(link):
	title = re.search('.*\.\.\.', link)
	title = title.replace('...', '').replace('/', '')
	realLink = re.search('\.\.\..*')
	realLink = realLink.replace('...', '')
	subprocess.call(['curl', link, '-o', dest + title + '.jpg'])


if __name__ == '__main__':
	if '--bad' in sys.argv:
		# dest = '/media/sf_redDrive/reddit/'
		dest = ''
	else:
		dest = input('Location to download images to: ')
	scrapedLinks = []

	pool = mp.Pool(3)

	print('Starting browser.\n')
	scraper = Reddit()
	scrapedLinks = scraper.getLinks()
	print(scrapedLinks)
	if scrapedLinks is None:
		print('Probably broken ip :/')
		scraper.driver.close()
		exit()
	if len(scrapedLinks) > 0:
		print('Found ' + str(len(scrapedLinks)) + ' links. Now downloading them.')
		pool.map(curlLinks, scrapedLinks)







