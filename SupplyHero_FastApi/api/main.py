from fastapi import FastAPI, File, UploadFile, Depends, HTTPException
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users import FastAPIUsers
from pdf2image import convert_from_bytes
from typing import Optional

from db.mongo import MongoSession
from model.user import *
from api.config import jwt_authentication

try:
    from PIL import Image
except ImportError:
    import Image
import pytesseract


# Database for users
mongo_db_users = MongoSession(collection='users')
user_db = MongoDBUserDatabase(UserDB, mongo_db_users.collection)

# Database for school supply list
mongo_db_supplies = MongoSession(collection='school_supplies')

# Backend FastAPI Server Declaration 
app = FastAPI()

# User Management
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)

origins = [
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Router to /login endpoint More info: https://frankie567.github.io/fastapi-users/configuration/routers/auth/
app.include_router(
    fastapi_users.get_auth_router(jwt_authentication), tags=["auth"]
)

# Router to /register endpoint More info: https://frankie567.github.io/fastapi-users/configuration/routers/register/
app.include_router(
    fastapi_users.get_register_router(), tags=["auth"]
)


@app.post("/upload")
async def create_uploaded_file(user: User=Depends(fastapi_users.get_current_active_user), file: UploadFile = File(...)):
    # Retrieve school supplies
    if file.content_type == 'image/jpeg' or file.content_type == 'image/png':
        supply_str = pytesseract.image_to_string(Image.open(file.file)).splitlines()
    elif file.content_type == 'application/pdf': # Will need Poppler
        image_obj = convert_from_bytes(file.file.read())
        if len(image_obj) > 1:
            raise HTTPException(status_code=400, detail="PDF contains more than 1 page.")
        supply_str = pytesseract.image_to_string(image_obj[0]).splitlines()
    else:
        raise HTTPException(status_code=400, detail="File is not an image.")
    supply_str = [elem for elem in supply_str if elem]

    # Store data to database
    supplies_data = {'email': user.email, 'filename': file.filename , 'school_supplies': supply_str}
    supplies_data = mongo_db_supplies.insert_json(supplies_data)
    if supplies_data:
        return {"Message": "Success"}
    else:
        raise HTTPException(status_code=400, detail="Could not send data to database.")


@app.get("/")
async def main(user: User=Depends(fastapi_users.get_current_active_user)):
    return {'username': user.email,
            'pass': user.hashed_password}
