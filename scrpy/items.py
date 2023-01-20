# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy

class NoutItem(scrapy.Item):
    url = scrapy.Field()
    date = scrapy.Field()
    name = scrapy.Field()
    processor = scrapy.Field()
    core = scrapy.Field()
    mhz = scrapy.Field()
    ram = scrapy.Field()
    screen = scrapy.Field()
    price = scrapy.Field()
