import pymongo

DEFAULT_DB_URL = "mongodb://localhost:27017/"

class MongoClient(object):
    def __init__(self, db: str, collection: str, url: str=DEFAULT_DB_URL) -> None:
        self.client = pymongo.MongoClient(url)
        self.db = self.client.get_database(db)
        self.col = self.db.get_collection(collection)

    def add_computer(self, computer):
        self.col.update_one({'ip': computer['ip']}, {'$set': computer}, upsert=True)

    def get_all_computers(self):
        return self.col.find({})