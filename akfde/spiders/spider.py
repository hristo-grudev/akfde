import re

import scrapy

from scrapy.loader import ItemLoader

from ..items import AkfdeItem
from itemloaders.processors import TakeFirst


class AkfdeSpider(scrapy.Spider):
	name = 'akfde'
	start_urls = ['https://www.akf.de/unser-unternehmen/aktuelles/']

	def parse(self, response):
		post_links = response.xpath('//a[contains(@class, "more")]/@href').getall()
		yield from response.follow_all(post_links, self.parse_post)

	def parse_post(self, response):
		title = response.xpath('//h1[@class="text-center"]/text()').get()
		description = response.xpath('//p//text()[normalize-space() and not(ancestor::div[@class="header-contactform popup_46"])]').getall()
		description = [p.strip() for p in description]
		description = ' '.join(description).strip()
		try:
			date = re.findall(r'\d{1,2}\.\s[a-zA-ZäöüÄÖÜß]+\s\d{4}', description)[0]
		except:
			date = ''

		item = ItemLoader(item=AkfdeItem(), response=response)
		item.default_output_processor = TakeFirst()
		item.add_value('title', title)
		item.add_value('description', description)
		item.add_value('date', date)

		return item.load_item()
