import pymongo
import sqlite3
from nltk.tokenize import word_tokenize


class EnigmaSpiderPipeline:
    def __init__(self):
        self.conn = pymongo.MongoClient('localhost', 27017)
        database = self.conn['enigma']
        self.enigma = database['crawled_pages']
        self.enigma_images = database['crawled_images']

    def process_item(self, item, spider):
        self.dict_builder(item)
        enigma_info = {
            'url': item['url'],
            'domain': item['domain'],
            'page_title': item['page_title'],
            'meta_tags': item['meta_tags'],
            'html_body': item['html_body'],
            'word_dictionary': item['word_dictionary']
        }
        self.enigma.insert(enigma_info)
        return item

    def dict_builder(self, item):
        word_dictionary = {}
        for word in word_tokenize(item['html_body']):
            if word.islower():
                if word in word_dictionary:
                    word_dictionary[word] += 1
                else:
                    word_dictionary[word] = 1
        item['word_dictionary'] = word_dictionary
        return item


class DefaultValuesPipeline(object):
    def process_item(self, item, spider):
        item.setdefault('meta_tags', [])
        return item


class StoreSQLPipeline:
    def process_item(self, item, spider):
        conn = sqlite3.connect('../data-center/library/enigma.sqlite')
        cursor = conn.cursor()

        cursor.execute('''CREATE TABLE IF NOT EXISTS Pages
            (id INTEGER PRIMARY KEY, url TEXT UNIQUE, html TEXT,
             old_rank REAL, new_rank REAL)''')

        cursor.execute('''CREATE TABLE IF NOT EXISTS Links
            (from_id INTEGER, to_id INTEGER, UNIQUE(from_id, to_id))''')

        url = item['url']
        html = item['html_body'][:256]
        links = item['links']

        cursor.execute('''INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES (?, ?, 1.0)''', (url, html, ))
        conn.commit()

        cursor.execute('SELECT id FROM Pages WHERE url=?', (url, ))
        row = cursor.fetchone()
        from_id = row[0]

        for link in links:
            cursor.execute('INSERT OR IGNORE INTO Pages (url, html, new_rank) VALUES ( ?, NULL, 1.0 )', (link, ))
            conn.commit()

            cursor.execute('SELECT id FROM Pages WHERE url=? LIMIT 1', (link, ))
            try:
                row = cursor.fetchone()
                to_id = row[0]
            except:
                continue
            cursor.execute('INSERT OR IGNORE INTO Links (from_id, to_id) VALUES ( ?, ? )', (from_id, to_id))

        cursor.close()
        return item
