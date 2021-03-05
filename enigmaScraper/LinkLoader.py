from pymongo import MongoClient


def load_urls():
    client = MongoClient('localhost', 27017)
    pipeline = [{
            "$unwind": "$links"
        },
        {
            "$match": {
                "url": {"$ne": "links"}
            }
        },
        {
            "$project": {"_id": 0, "links": 1}
        }]

    result = list(client['enigma']['crawled_pages'].aggregate(pipeline=pipeline))
    links = set()
    for item in result:
        links.add(item['links'])

    return list(links)


def load_domains():
    with open('allowed-domains.txt', 'r') as file:
        domains = file.read().splitlines()
    return domains
