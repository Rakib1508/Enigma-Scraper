import scrapy
from scrapy.loader import ItemLoader
from itemloaders.processors import TakeFirst, MapCompose, Join
from w3lib.html import remove_tags


def text_preprocessor(text):
    return ' '.join(text.split())


class EnigmaScraperItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field(
        output_processor=TakeFirst()
    )
    domain = scrapy.Field(
        output_processor=TakeFirst()
    )
    page_title = scrapy.Field(
        input_processor=MapCompose(remove_tags),
        output_processor=TakeFirst()
    )
    meta_tags = scrapy.Field(
        output_processor=TakeFirst()
    )
    html_body = scrapy.Field(
        input_processor=MapCompose(remove_tags, text_preprocessor),
        output_processor=TakeFirst()
    )
    links = scrapy.Field()
    images = scrapy.Field()
