import uuid

import pytesseract
from db.mongo import MongoSession, MongoSessionRegular
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from model.user import User
from pdf2image import convert_from_bytes
from PIL import Image

from api.auth import fastapi_users

router = APIRouter()

# Database for school supply list
supplies_metadata_db = MongoSessionRegular(
    collection="school_supplies_metadata")
mongo_db_supplies = MongoSessionRegular(collection="school_supplies")


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

    # Store Metadata for Supply List & Data for Supply List
    # Generate a unique UUID based on string
    supply_uuid = uuid.uuid5(uuid.NAMESPACE_OID, ''.join(supply_arr))

    # Metadata to DB
    metadata_update_result = supplies_metadata_db.upsert_supply_list_metadata(
        user, supply_uuid
    )

    # Supply List Data to DB
    supply_list_data = {
        "id": supply_uuid,
        "list_of_supplies": supply_arr,
        "admin_ids": {"id": user.id},
        "read_only_ids": {"id": user.id}
    }
    mongo_db_supplies.upsert_supply_list(supply_list_data)

    if not metadata_update_result.upserted_id and metadata_update_result.modified_count == 0:
        raise HTTPException(
            status_code=400, detail="Data already exists in DB")
    else:
        return {"Message": "Success",
                "school_supply_id": supply_uuid}
