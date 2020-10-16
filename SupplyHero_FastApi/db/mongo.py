from pymongo import MongoClient


class MongoSession:

    def __init__(self, database_name="supply-hero", collection=None):
        self.client = MongoClient(
            'mongodb+srv://admin_user:8w5B1e3hz4UcGEs5@supply-hero.isdcn.mongodb.net/supply-hero?retryWrites=true&w=majority')
        self.db = self.client['database_name']
        self.collection = self.db.user_accounts['collection']

    def insert_json(self, document):
        self.collection.insert_one(document)

    def authenticate(self, document):
        isAuthenticated = False
        record = self.collection.find_one({"email": document.email})
        if record:
            if record.password == document.password:
                isAuthenticated = True

        return isAuthenticated


# example of a mongoSession
db_school_supply = MongoSession('school-supply-list')
