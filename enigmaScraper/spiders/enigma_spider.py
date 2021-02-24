import scrapy
from urllib.parse import urljoin, urlparse
from ..items import EnigmaScraperItem
from scrapy.loader import ItemLoader


class EnigmaSpider(scrapy.Spider):
    # unique name to call the spider
    name = "enigma"

    def start_requests(self) -> 'response':
        """
        when the spider is run, this method is called which access all the necessary
        settings to complete the request format. And then the method sends the request
        to spider -> engine -> downloaderMiddleware -> downloader. Finally,
        the downloader makes the request to the distant server.
        """
        urls = [
            # 'https://quotes.toscrape.com/',
            'https://en.wikipedia.org/wiki/Apple_Inc.',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    """def parser(self, response: bytes) -> 'response_parser':
        
        spider sends request to the downloader from the engine which was taken from the
        scheduler where all the requests are queued to be called. Once the downloader
        completes the request, a response is generated. That request is then sent to the
        spider using downloader -> downloaderMiddleware -> engine -> spiderMiddleware ->
        spider. And this method is called to parse the response.
        
        url = response.url
        content_type = str(response.headers['content-type'], encoding='UTF-8')
        last_modified = str(response.headers['last-modified'], encoding='UTF-8')
        page_title = response.xpath('string(//title)').get()
        meta_tags = response.css('meta').getall()
        html_body = response.xpath('string(//body)').get()
        page_links = set(response.css('a::attr(href)').getall())
        page_images = set(response.css('img::attr(src)').getall())

        domain = self.get_domain(url)
        links = self.get_absolute_url(url, page_links)
        images = self.get_absolute_url(url, page_images)

        items = EnigmaScraperItem()
        items['url'] = url
        items['domain'] = domain
        items['content_type'] = content_type
        items['last_modified'] = last_modified
        items['page_title'] = page_title
        items['meta_tags'] = meta_tags
        items['html_body'] = html_body
        items['links'] = links
        items['images'] = images

        yield items

        # yield from response.follow_all(css='a', callback=self.parse)
"""
    def get_domain(self, url):
        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain

    def get_absolute_url(self, base_url, urls):
        links = []
        for url in urls:
            links.append(urljoin(base_url, url))
        return links

    def parse(self, response: bytes) -> 'response_parser':
        meta_tags = dict()
        for element in response.xpath('//head/meta'):
            for index, attribute in enumerate(element.xpath('@*'), start=1):
                attribute_name = element.xpath('name(@*[%d])' % index).extract_first()
                meta_tags[attribute_name] = attribute.extract()
        # meta_tags = dict(attributes)

        page_links = set(response.css('a::attr(href)').getall())
        page_images = set(response.css('img::attr(src)').getall())

        links = self.get_absolute_url(response.url, page_links)
        images = self.get_absolute_url(response.url, page_images)

        items = ItemLoader(item=EnigmaScraperItem(), response=response)
        items.add_value('url', response.url)
        items.add_value('domain', self.get_domain(response.url))
        items.add_value('meta_tags', meta_tags)
        items.add_css('page_title', 'title')
        items.add_css('html_body', 'body')
        items.add_value('links', links)
        items.add_value('images', images)

        yield items.load_item()
