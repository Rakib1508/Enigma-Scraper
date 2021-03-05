import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, remove_tags_with_content
from nltk.corpus import stopwords
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize



def script_tag_remover(html):
    return str(remove_tags_with_content(html, ('script',)))


def text_preprocessor(text):
    return ' '.join(text.split())


def drop_stopwords(text):
    stop_words = stopwords.words('english')
    words = []
    for word in word_tokenize(text):
        if word not in stop_words and word.isalnum():
            words.append(word)
    return ' '.join(words)


def stemmer(text):
    words = []
    ps = PorterStemmer()
    for word in word_tokenize(text):
        words.append(ps.stem(word))
    return ' '.join(words)


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
    content = scrapy.Field(
        input_processor=MapCompose(
            script_tag_remover, remove_tags, text_preprocessor,
        ),
        output_processor=TakeFirst()
    )
    content_length = scrapy.Field()
    word_dictionary = scrapy.Field(
        input_processor=MapCompose(
            script_tag_remover, remove_tags, text_preprocessor, drop_stopwords, stemmer,
        ),
        output_processor=TakeFirst()
    )
    links = scrapy.Field()
    old_rank = scrapy.Field(output_processor=TakeFirst())
    new_rank = scrapy.Field(output_processor=TakeFirst())
