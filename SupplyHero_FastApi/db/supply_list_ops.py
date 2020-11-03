from db.mongo import db
from bson import ObjectId


def user_helper(supply_list) -> dict:
    return {
        "id": str(supply_list["_id"]),
        "list_name": supply_list["list_name"],
        "list_of_supplies": supply_list["list_of_supplies"],
        "admin_ids": supply_list["_admin_ids"],
        "read_only_ids": supply_list["_read_only_ids"],
    }


# Retrieve all supply lists present in the database
def retrieve_supply_list_all():
    supply_lists = []
    for supply_list in db.collection.find():
        supply_lists.append(user_helper(supply_list))
    return supply_lists


# Retrieve a supply list with a matching ID
def retrieve_supply_list(user_id):
    # get lists that this user can view
    supply_lists_reg = []
    for supply_list in db.collection.find({"_read_only_ids": user_id}):
        supply_lists_reg.append(user_helper(supply_list))

    # get lists that this user can edit
    supply_list_admin = []
    for supply_list in db.collection.find({"_admin_ids": user_id}):
        supply_list_admin.append(user_helper(supply_list))

    # get unique supply lists only
    return list(set(supply_lists_reg + supply_list))


# Add a new supply list into to the database
def add_supply_list(supply_list_data):
    supply_list = db.collection.insert_one(supply_list_data)
    new_supply_list = db.collection.find_one({"_id": supply_list.inserted_id})
    return user_helper(new_supply_list)


# Update a supply list with a matching ID
def update_supply_list(admin_id, supply_list_data):
    is_updated = False

    # Return false if an empty request body is sent.
    if len(supply_list_data) < 1:
        return is_updated
    supply_list = db.collection.find_one({"_admin_ids": ObjectId(admin_id)})
    if supply_list:
        updated_supply_list = db.collection.update_one(
            {"_admin_ids": ObjectId(admin_id)}, {"$set": supply_list_data}
        )
        if updated_supply_list:
            is_updated = True

    return is_updated

# Delete a supply list from the database


def delete_supply_list(supply_list_id, admin_id):
    is_deleted = False
    supply_list = db.collection.find_one(
        {"_id": ObjectId(supply_list_id), "_admin_ids": ObjectId(admin_id)})
    if supply_list:
        # update all users that have access to this supply list
        db.collection.update(
            {"school_supplies_ids": ObjectId(supply_list_id)},
            {"$pull": {
                "school_supplies_ids": supply_list_id}},
        )

        # delete the supply list
        db.collection.delete_one({"_id": ObjectId(supply_list_id)})

        # supply is only "deleted" if no user has link to it and it is deleted from db
        is_deleted = True

    return is_deleted
