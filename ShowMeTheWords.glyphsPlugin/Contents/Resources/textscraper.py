import os, re, random
import scrapy
from scrapy.exceptions import CloseSpider
from filereader import loadWords

class WordSpider(scrapy.Spider):
	name = 'Word sample collector'
	start_urls = ['https://www.wikipedia.org']

	def parse(self, response):
		langs = ["pl", "es", "de", "en", "it", "fi"]
		lang = random.choice(langs)

		text = response.css('#mw-content-text p::text').extract()
		if text:
			for t in text:
				for word in re.compile("\s").split(t):
					yield {
						'word': word
					}

		for next_page in response.css('a[lang="' + lang + '"], #mw-content-text a'):
			yield response.follow(next_page, self.parse)