import pymongo
from nltk.tokenize import word_tokenize


class EnigmaSpiderPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        database = self.conn['enigma']
        self.enigma = database['crawled_pages']

    def process_item(self, item, spider):
        item['content_length'] = len(item['content'].split())
        item['content'] = item['content'][:1024]
        self.dict_builder(item)
        self.enigma.insert(dict(item))
        return item

    def dict_builder(self, item):
        word_dictionary = {}
        for word in word_tokenize(item['word_dictionary']):
            if word.islower() and word.isalpha():
                if word in word_dictionary:
                    word_dictionary[word] += 1
                else:
                    word_dictionary[word] = 1
        dictionary = dict()
        for key in word_dictionary:
            dictionary[key] = {}
            dictionary[key]['count'] = word_dictionary[key]
            dictionary[key]['tf'] = word_dictionary[key] / item['content_length']
            dictionary[key]['idf'] = 0.0
            dictionary[key]['tfidf'] = 0.0
        item['word_dictionary'] = dictionary
        return item


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        item.setdefault('meta_tags', [])
        return item
