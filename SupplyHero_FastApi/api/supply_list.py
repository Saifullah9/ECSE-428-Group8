import pytesseract
from db.mongo import MongoSession
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from model.user import User
from pdf2image import convert_from_bytes
from PIL import Image

from api.auth import fastapi_users

router = APIRouter()

# Database for school supply list
mongo_db_supplies = MongoSession(collection='school_supplies')


@router.post("/upload")
async def create_uploaded_file(user: User = Depends(fastapi_users.get_current_active_user),
                               file: UploadFile = File(...)):
    # Retrieve school supplies
    if file.content_type == 'image/jpeg' or file.content_type == 'image/png':
        supply_str = pytesseract.image_to_string(
            Image.open(file.file)).splitlines()
    elif file.content_type == 'application/pdf':  # Will need Poppler
        image_obj = convert_from_bytes(file.file.read())
        if len(image_obj) > 1:
            raise HTTPException(
                status_code=400, detail="PDF contains more than 1 page.")
        supply_str = pytesseract.image_to_string(image_obj[0]).splitlines()
    else:
        raise HTTPException(status_code=400, detail="File is not an image.")
    supply_str = [elem for elem in supply_str if elem]

    # Store data to database
    supplies_data = {'email': user.email,
                     'filename': file.filename, 'school_supplies': supply_str}
    supplies_data = mongo_db_supplies.insert_json(supplies_data)
    if supplies_data:
        return {"Message": "Success"}
    else:
        raise HTTPException(
            status_code=400, detail="Could not send data to database.")
