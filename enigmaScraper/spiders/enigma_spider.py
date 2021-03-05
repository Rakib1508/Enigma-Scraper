import scrapy
import validators
from urllib.parse import urljoin, urlparse
from ..items import EnigmaScraperItem
from scrapy.loader import ItemLoader
from ..LinkLoader import load_urls, load_domains


class EnigmaSpider(scrapy.Spider):
    # unique name to call the spider
    name = 'enigma'
    start_urls = load_urls()
    allowed_domains = load_domains()

    """def start_requests(self) -> 'response':
        when the spider is run, this method is called which access all the necessary
        settings to complete the request format. And then the method sends the request
        to spider -> engine -> downloaderMiddleware -> downloader. Finally,
        the downloader makes the request to the distant server.

        urls = [
            'https://en.wikipedia.org/wiki/Apple_Inc.',
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)"""

    def parse(self, response: bytes) -> 'response_parser':
        """spider sends request to the downloader from the engine which was taken from the
        scheduler where all the requests are queued to be called. Once the downloader
        completes the request, a response is generated. That request is then sent to the
        spider using downloader -> downloaderMiddleware -> engine -> spiderMiddleware ->
        spider. And this method is called to parse the response."""

        meta_tags = dict()
        # this for loop traverses each of the meta tags inside the head tag of the HTML file
        # it will collect each of the meta attributes along with its value
        for element in response.xpath('//head/meta'):
            for index, attribute in enumerate(element.xpath('@*'), start=1):
                attribute_name = element.xpath('name(@*[%d])' % index).extract_first()
                meta_tags[attribute_name] = attribute.extract()

        # get links of all the links (href) and images (src)
        page_links = set(response.css('a::attr(href)').getall())

        # call methods to convert the relative urls into absolute urls
        links = self.get_absolute_url(response.url, page_links)

        # ItemLoader object passes the values in different fields of the Item class
        # ItemLoader is used in order to preprocess the values before containing
        # in the Item object.
        items = ItemLoader(item=EnigmaScraperItem(), response=response)
        items.add_value('url', response.url)
        items.add_value('domain', self.get_domain(response.url))
        items.add_value('meta_tags', meta_tags)
        items.add_css('page_title', 'title')
        items.add_css('content', 'body')
        items.add_value('content_length', 1)
        items.add_css('word_dictionary', 'body')
        items.add_value('links', links)
        items.add_value('old_rank', 0.0)
        items.add_value('new_rank', 1.0)

        yield items.load_item()

        for url in links:
            yield scrapy.Request(url, callback=self.parse)

    def get_domain(self, url: 'string') -> 'string':
        """This function requires one parameter, i.e. unique URL of any webpage.
        This is always an absolute URL from which the domain name for this
        particular website will be extracted."""

        parsed_uri = urlparse(url)
        domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
        return domain

    def get_absolute_url(self, base_url: 'string', urls: 'string') -> list:
        """This function provides functionality to complete a relative URL retrieved
        from an anchor tag or an image tag of an HTML document. Then the base URL, i.e.
        the URL of that particular page is appended in front of it the generate the
        absolute URL for the linked page or any image."""
        links = []
        for url in urls:
            if url == base_url:
                continue
            links.append(urljoin(base_url, url))
        return self.url_preprocessor(links)

    def url_preprocessor(self, items):
        urls = []
        for item in items:
            if item.count(':') > 1:
                continue
            if '#' not in item and '@' not in item:
                if validators.url(item):
                    urls.append(item)
        return urls
