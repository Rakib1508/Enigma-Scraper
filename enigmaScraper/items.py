import scrapy
from itemloaders.processors import TakeFirst, MapCompose
from w3lib.html import remove_tags, remove_tags_with_content
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.stem import WordNetLemmatizer
from nltk.tokenize import word_tokenize
from nltk.corpus import wordnet


def get_wordnet_pos(word):
    """Map POS tag to first character lemmatize() accepts"""
    tag = pos_tag([word])[0][1][0].upper()
    tag_dict = {"J": wordnet.ADJ,
                "N": wordnet.NOUN,
                "V": wordnet.VERB,
                "R": wordnet.ADV}
    return tag_dict.get(tag, wordnet.NOUN)


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


def lemmatizer(text):
    words = []
    lm = WordNetLemmatizer()
    for word in word_tokenize(text):
        words.append(lm.lemmatize(word, get_wordnet_pos(word)))
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
            script_tag_remover, remove_tags, text_preprocessor, lemmatizer, drop_stopwords,
        ),
        output_processor=TakeFirst()
    )
    links = scrapy.Field()
    old_rank = scrapy.Field(output_processor=TakeFirst())
    new_rank = scrapy.Field(output_processor=TakeFirst())
