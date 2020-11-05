from pymongo import MongoClient
import motor.motor_asyncio


class MongoSession:
    def __init__(self, collection=None, database_name="supply-hero"):
        DATABASE_URL = "mongodb+srv://admin_user:8w5B1e3hz4UcGEs5@supply-hero.isdcn.mongodb.net/supply-hero?retryWrites=true&w=majority"
        self.client = motor.motor_asyncio.AsyncIOMotorClient(
            DATABASE_URL, uuidRepresentation="standard"
        )
        self.db = self.client[database_name]
        self.collection = self.db[collection]

    def insert_json(self, document):
        return self.collection.insert_one(document)

    def find_json(self, document):
        return self.collection.find_one(document)

    def delete_json(self, document):
        return self.collection.delete_one(document)


class MongoSessionRegular:
    def __init__(self, collection=None, database_name="supply-hero"):
        DATABASE_URL = "mongodb+srv://admin_user:8w5B1e3hz4UcGEs5@supply-hero.isdcn.mongodb.net/supply-hero?retryWrites=true&w=majority"
        self.client = MongoClient(DATABASE_URL, uuidRepresentation="standard")
        self.db = self.client[database_name]
        self.collection = self.db[collection]

    def insert_json(self, document):
        return self.collection.insert_one(document)

    def find_json(self, document, args=None):
        return self.collection.find_one(document, args)

    def delete_json(self, document):
        return self.collection.delete_one(document)

    def upsert_supply_list_metadata(self, user, supply_uuid):
        update_result = self.collection.update_one(
            {
                "$and": [
                    {"email": user.email},
                    {"school_supply_ids": {"$nin": [supply_uuid]}},
                ]
            },
            {"$push": {"school_supply_ids": supply_uuid}},
            upsert=False,
        )
        if update_result.modified_count > 0:
            return update_result
        else:
            return self.collection.update_one(
                {"email": user.email},
                {
                    "$setOnInsert": {
                        "email": user.email,
                        "school_supply_ids": [supply_uuid],
                    }
                },
                upsert=True,
            )

    def upsert_supply_list(self, supply_list_data):
        return self.collection.update_one(
            {"id": supply_list_data["id"]},
            {"$setOnInsert": supply_list_data},
            upsert=True,
        )

    def remove_supply_list_metadata(self, email, supply_uuid):
        return self.collection.update_one(
            {"email": email},
            {"$pull": {"school_supply_ids": supply_uuid}},
            upsert=False,
        )

    def remove_supply_list(self, supply_uuid):
        return self.collection.delete_one({"id": supply_uuid})

    def logout_active_user(self, user):
        self.collection.update_one(
            {"email": user.email},
            {"$set": {"is_active": "false"}}
        )
        return {"user_email": user.email,
                "logout_success": "true"}
