import sqlite3


def load_urls():
    conn = sqlite3.connect('../data-center/library/enigma.sqlite')
    cursor = conn.cursor()

    cursor.execute('SELECT url FROM Pages WHERE html is NULL ORDER BY RANDOM() LIMIT 1000')
    links = cursor.fetchall()

    urls = []
    for link in links:
        urls.append(link[0])

    return urls
