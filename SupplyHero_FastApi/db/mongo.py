from pymongo import MongoClient


class MongoSession:
    
    def __init__(self, database_name, collection):
        self.client = MongoClient('mongodb+srv://admin_user:8w5B1e3hz4UcGEs5@supply-hero.isdcn.mongodb.net/supply-hero?retryWrites=true&w=majority')
        self.db = self.client['database_name']
        self.collection = self.db.user_accounts['collection']

    def insert_json(self, document):
        self.collection.insert_one(document)

db = MongoSession('supply-hero', 'school-supply-list')



