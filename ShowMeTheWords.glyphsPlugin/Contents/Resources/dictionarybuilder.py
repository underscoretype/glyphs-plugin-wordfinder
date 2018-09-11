"""
A module that helps retrieving new words via a webscrape



"""
import scrapy
from scrapy.crawler import CrawlerProcess
from textscraper import WordSpider


# 0020 — 007F  	Basic Latin
# 00A0 — 00FF  	Latin-1 Supplement
# 0100 — 017F  	Latin Extended-A
# 0180 — 024F  	Latin Extended-B
# 0370 — 03FF  	Greek and Coptic
# 0400 — 04FF  	Cyrillic
# 0500 — 052F  	Cyrillic Supplementary

ranges = {
	"latin":    ["0020", "024F"],
	"greek":    ["0370", "03FF"],
	"cyrillic": ["0500", "052F"]
}



def scapeForWords(rangeId):
	"""
	Start a new scraping session that collects words for the range, saves them,
	analyses the findings and generates a new file for the range containing new
	additions
	"""
	#startScraper()
	#filterResults()
	#storeResults()

def startScraper():
	print "starting scraper"
	process = CrawlerProcess({
	    'USER_AGENT': 'Mozilla/4.0 (compatible; MSIE 7.0; Windows NT 5.1)'
	})

	process.crawl(WordSpider)
	process.start()
	print "done scraping"



if __name__ == "__main__":
	scapeForWords("latin")


