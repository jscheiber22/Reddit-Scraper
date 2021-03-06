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
		chrome_options.add_argument("--headless")
		self.driver = uc.Chrome(options=chrome_options)

	def getLinks(self, subreddit):
		# Skips subreddit if it starts with # so that they can be commented out in list
		if subreddit.startswith('#'):
			return
		links = []

		subreddit = subreddit.replace('\n', '')

		used = os.listdir(dest + subreddit)

		print('Opening ' + subreddit + '.\n')
		self.driver.get('https://www.reddit.com/r/' + subreddit + '/')
		sleep(3)
		self.driver.get('https://www.reddit.com/r/' + subreddit + '/')
		sleep(3)

		try:
			self.driver.find_element_by_xpath('//button[text()="Yes"]').click()
			sleep(3)
		except:
			pass

		self.scroll_down()

		images = self.driver.find_elements_by_xpath('//img')
		for image in images:
			src = image.get_attribute('src')
			if src is not None:
				if 'preview' in src and not 'award_images' in src:
					title = image.find_element_by_xpath('./../../..').get_attribute('href')
					if title is not None:
						title = re.search('/comments/.*/.*/', title)
						if title is not None:
							title = title.group().replace('/comments/', '')
							title = re.search('/.*/', title)
							if title is not None:
								if not title.group().replace('/', '') + '.jpg' in used:
									links.append(subreddit + '###' + title.group() + '...' + src)

		if len(links) > 0:
			print('Found ' + str(len(links)) + ' in ' + subreddit + ' sub. Now downloading them...')
			self.driver.close()
			for link in links:
				curlLinks(link)
			return 1 # self.pullLinks
		else:
			print('Pulled no links from ' + subreddit + ' :/')
			self.driver.close()


	def scroll_down(self):
		"""A method for scrolling the page."""

		# Get scroll height.
		last_height = self.driver.execute_script("return document.body.scrollHeight")

		for x in range(0, 25):

			# Scroll down to the bottom.
			self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")

			# Wait to load the page.
			sleep(5)

			# Calculate new scroll height and compare with last scroll height.
			new_height = self.driver.execute_script("return document.body.scrollHeight")

			if new_height == last_height:

				break

			last_height = new_height


MAX_SEARCH_CPU_CORES = 3

def start(searchTerm):
	if searchTerm is not None and searchTerm != '':
		scraper = Reddit()
		scrapedLinks = scraper.getLinks(searchTerm)
		return 1

def curlLinks(link):
	subreddit = re.search('.*###', link)
	if subreddit is not None:
		subreddit = subreddit.group().replace('###', '')
		title = re.search('###.*\.\.\.', link)
		if title is not None:
			title = title.group().replace('...', '').replace('/', '').replace('###', '')
			realLink = re.search('\.\.\..*', link)
			if realLink is not None:
				realLink = realLink.group().replace('...', '')
				print('\nCurling ' + title + ' from ' + subreddit + '.')
				subprocess.call(['curl', realLink, '-o', dest + subreddit + '/' + title + '.jpg'])


if __name__ == '__main__':
	dest = '/media/sf_redDrive/reddit/'
	scrapedLinks = []
	scrapedLinksFinal = []

	f = open('toSearch', 'r')
	subreddits = f.readlines()
	f.close()

	for subred in subreddits:
		subred = subred.replace('\n', '')
		if not os.path.isdir(dest + subred) and not subred.startswith('#'):
			os.mkdir(dest + subred)

	pool = mp.Pool(MAX_SEARCH_CPU_CORES) # 2

	print('Opening browsers.\n')
	scrapedLinks = pool.map(start, subreddits)

	sleep(10)
	# Wait for everything to end and then kill all the chromes
	subprocess.call('killall chrome', shell=True)







