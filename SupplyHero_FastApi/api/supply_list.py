import uuid

import pytesseract
from db.mongo import MongoSession, MongoSessionRegular
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from model.supply_list import SupplyList
from model.user import User
from model.supply_list import SupplyListPrivilege
from pdf2image import convert_from_bytes
from PIL import Image
from pydantic import BaseModel

import uuid
from api.auth import fastapi_users

router = APIRouter()

# Database for school supply list
supplies_metadata_db = MongoSessionRegular(
    collection="school_supplies_metadata")
mongo_db_supplies = MongoSessionRegular(collection="school_supplies")
mongo_db_users = MongoSessionRegular(collection="users")


@router.post("/upload")
async def create_uploaded_file(
    user: User = Depends(fastapi_users.get_current_active_user),
    file: UploadFile = File(...),
):
    # Retrieve school supplies
    if file.content_type == "image/jpeg" or file.content_type == "image/png":
        supply_str = pytesseract.image_to_string(Image.open(file.file))
        supply_arr = supply_str.splitlines()
    elif file.content_type == "application/pdf":  # Will need Poppler
        image_obj = convert_from_bytes(file.file.read())
        if len(image_obj) > 1:
            raise HTTPException(
                status_code=400, detail="PDF contains more than 1 page."
            )
        supply_str = pytesseract.image_to_string(image_obj[0])
        supply_arr = supply_str.splitlines()
    else:
        raise HTTPException(status_code=400, detail="File is not an image.")
    supply_arr = [elem for elem in supply_arr if elem]
    checklist_marker = [False] * len(supply_arr)
    # Store Metadata for Supply List & Data for Supply List
    # Generate a unique UUID based on string
    supply_uuid = uuid.uuid5(uuid.NAMESPACE_OID, ''.join(supply_arr))

    # Metadata to DB
    metadata_update_result = supplies_metadata_db.upsert_supply_list_metadata(
        user, supply_uuid, checklist_marker
    )

    # Supply List Data to DB
    supply_list_data = {
        "id": supply_uuid,
        "list_of_supplies": supply_arr,
        "admin_ids": [user.id],
        "read_only_ids": [user.id]
    }
    mongo_db_supplies.upsert_supply_list(supply_list_data)

    if not metadata_update_result.upserted_id and metadata_update_result.modified_count == 0:
        raise HTTPException(
            status_code=400, detail="Data already exists in DB")
    else:
        return {"Message": "Success",
                "school_supply_id": supply_uuid}


@router.get("/download")
async def get_all_lists(
    user: User = Depends(fastapi_users.get_current_active_user)
):
    # Retrieve User's Supply List Metadata from DB
    query = {"email": user.email}
    user_supply_ids = supplies_metadata_db.find_json(query)
    response = {"Message": "Success",
                "supply_lists": []}

    # Retrieve all Supply List Data from DB Based On Lists' IDs
    if user_supply_ids:
        supply_ids = user_supply_ids["school_supply_ids"]
        lists = [mongo_db_supplies.find_json(
            {"id": id}, {"_id": 0}) for id in supply_ids]
        for list_index, supply_list in enumerate(lists):
            supply_list['list_of_supplies'] = [[item, user_supply_ids["school_supply_checklist"][list_index][item_index]] for item_index, item in enumerate(supply_list['list_of_supplies'])]
        response["supply_lists"] = lists
        return response
    else:
        raise HTTPException(
            status_code=400, detail="No file has been uploaded.")


@router.post("/addUser")
async def create_uploaded_file(
    supply_list_priv: SupplyListPrivilege,
):
    # Given an email address, privilege_type, and supplyList_id
    # eg.
    # {
    # "email": "targetuser@gmail.com",
    # "privilege_type": "READ_ONLY",
    # "supply_list_id": "c074a20e-5025-5814-996f-af2efe1939a4"
    # }

    # Assume that user had admin rights (TODO: handled by FRONTEND)
    target_user = mongo_db_users.find_json(
        {"email": supply_list_priv.email})
    if target_user:
        supply_list = mongo_db_supplies.find_json(
            {"id": supply_list_priv.supply_list_id})
        if supply_list:
            if supply_list_priv.privilege_type == "ADMIN" or supply_list_priv.privilege_type == "READ_ONLY":
                mongo_db_supplies.add_supply_list_privilege(
                    target_user['id'], supply_list['id'], supply_list_priv.privilege_type)
                return {"Message": "Success",
                        "id": supply_list['id'],
                        }
            else:  # TODO not needed as the FRONTEND can only provide with 2 options
                raise HTTPException(
                    status_code=400, detail="The designated privilege does not exist")
        else:  # TODO not needed as the FRONTEND can only provide with the supply lists where I have admin rights
            raise HTTPException(
                status_code=400, detail="That supply list does not exist")

    else:
        raise HTTPException(
            status_code=400, detail="Target user (" +
            supply_list_priv.email + ") does not exist")


@router.put("/upload")
async def edit_uploaded_list(
    supply_list: SupplyList,
    user: User = Depends(fastapi_users.get_current_active_user)
):
    new_uuid = uuid.uuid5(uuid.NAMESPACE_OID, ''.join(supply_list.list_of_supplies))

    # If content is the same don't edit
    if new_uuid == supply_list.old_id:
        raise HTTPException(status_code=400, detail="The school supply list is the same")

    else:
        # Update school supplies metadata
        metadata_update_result = supplies_metadata_db.edit_supply_list_metadata(
            user, supply_list.old_id, new_uuid
        )

        # Update school supply
        data_update_result = mongo_db_supplies.edit_supply_list(
            supply_list.old_id, new_uuid, supply_list.list_of_supplies
        )
        if metadata_update_result.matched_count == 0 and data_update_result.matched_count == 0:
            raise HTTPException(status_code=400, detail=f'No School Supply list with ID: {supply_list.old_id}')

        return {"Message": "Success",
                "school_supply_id": new_uuid}

@router.delete("/List")
async def remove_supply_list_from_user(
        supply_list_id,
        email,
):
    id_to_remove = supply_list_id
    id_to_remove = uuid.UUID(id_to_remove)
    if supplies_metadata_db.remove_supply_list_metadata(email, id_to_remove).modified_count == 0:
        return {"Message": "No Changes Made"}
    else:
        return {"Message": "Success, id has been removed"}

