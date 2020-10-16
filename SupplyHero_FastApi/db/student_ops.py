from db.mongo import db
from bson import ObjectId

def student_helper(student) -> dict:
    return {
        "id": str(student["_id"]),
        "fullname": student["fullname"],
        "school_supplies": student["school_supplies"]
    }

# Retrieve all users present in the database
def get_students():
    students = []
    for student in db.collection.find():
        students.append(student_helper(student))
    return students


# Add a new student into to the database
def add_student(student_data: dict) -> dict:
    user = db.collection.insert_one(student_data)
    new_user = db.collection.find_one({"_id": user.inserted_id})
    return student_helper(new_user)


# Retrieve a student with a matching ID
def get_student(id: str) -> dict:
    user = db.collection.find_one({"_id": ObjectId(id)})
    if user:
        return student_helper(user)


# Update a student with a matching ID
def update_student(id: str, data: dict):
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
def delete_student(id: str):
    user = db.collection.find_one({"_id": ObjectId(id)})
    if user:
        db.collection.delete_one({"_id": ObjectId(id)})
        return True
