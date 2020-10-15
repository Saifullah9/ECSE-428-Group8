from db.mongo import db
from bson import ObjectId

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "fullname": user["fullname"],
        "username": user["email"],
        "email": user["email"],
        "password": user["password"],
        "students": user["students"]
    }

# Retrieve all users present in the database
def retrieve_users():
    users = []
    for user in db.collection.find():
        users.append(user_helper(user))
    return users


# Add a new student into to the database
def add_user(user_data: dict) -> dict:
    user = db.collection.insert_one(user_data)
    new_user = db.collection.find_one({"_id": user.inserted_id})
    return user_helper(new_user)


# Retrieve a student with a matching ID
def retrieve_user(id: str) -> dict:
    user = db.collection.find_one({"_id": ObjectId(id)})
    if user:
        return user_helper(user)


# Update a student with a matching ID
def update_user(id: str, data: dict):
    # Return false if an empty request body is sent.
    if len(data) < 1:
        return False
    user = db.collection.find_one({"_id": ObjectId(id)})
    if user:
        updated_user = db.collection.update_one(
            {"_id": ObjectId(id)}, {"$set": data}
        )
        if updated_user:
            return True
        return False


# Delete a student from the database
def delete_user(id: str):
    user = db.collection.find_one({"_id": ObjectId(id)})
    if user:
        db.collection.delete_one({"_id": ObjectId(id)})
        return True