import scrapy


class EnigmaScraperItem(scrapy.Item):
    # define the fields for your item here like:
    url = scrapy.Field()
    domain = scrapy.Field()
    content_type = scrapy.Field()
    last_modified = scrapy.Field()
    page_title = scrapy.Field()
    meta_tags = scrapy.Field()
    html_body = scrapy.Field()
    links = scrapy.Field()
    images = scrapy.Field()
