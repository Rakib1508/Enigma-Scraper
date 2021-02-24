import pymongo


class EnigmaSpiderPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        database = self.conn['enigma']
        self.collection = database['crawled_pages']

    def process_item(self, item, spider):
        self.collection.insert(dict(item))
        return item

    def text_preprocessor(self, text):
        pass
