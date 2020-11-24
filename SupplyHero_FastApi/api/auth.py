from db.mongo import MongoSession, MongoSessionRegular
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from fastapi_users.password import get_password_hash
from model.user import User, UserCreate, UserDB, UserUpdate
from fastapi import APIRouter, Depends, HTTPException
from api.config import jwt_authentication
from model.user import User

router2 = APIRouter()

# Database for users
mongo_db_users = MongoSession(collection="users")
mongo_db_users_reg = MongoSessionRegular(collection="users")
user_db = MongoDBUserDatabase(UserDB, mongo_db_users.collection)

# User Management
fastapi_users = FastAPIUsers(
    user_db,
    [jwt_authentication],
    User,
    UserCreate,
    UserUpdate,
    UserDB,
)


@router2.post("/logout")
async def logout_user(user: User = Depends(fastapi_users.get_current_active_user)):
    result = mongo_db_users_reg.logout_active_user(user)
    return result

@router2.put("/editProfile")
async def edit_user_profile(
    user_update: UserUpdate,
    user: User = Depends(fastapi_users.get_current_active_user)
):

    if user_update.email is None and user_update.password is None:
        raise HTTPException(status_code=400, detail="An email or password is needed.")

    current_email = user.email
    if user_update.email is not None:
        new_email = user_update.email
        user_in_db = mongo_db_users_reg.find_json({"email": new_email})
        if user_in_db is None:
            mongo_db_users_reg.collection.update_one(
                {"email": user.email}, 
                {"$set": {"email": new_email}}
            )
            current_email = new_email
        else:
            raise HTTPException(
            status_code=400, detail="Email is already used.")
    
    if user_update.password is not None:
        new_password = user_update.password
        hashed_password = get_password_hash(new_password)
        mongo_db_users_reg.collection.update_one(
            {"email": current_email}, 
            {"$set": {"hashed_password": hashed_password}}
        )
    
    return {"Message": "Success", "Email": current_email}


# @router2.post("/reactivate")
# async def reactivate_user(user: User = Depends(fastapi_users.get_current_user)):
#     result = mongo_db_users_reg.reactivate_user(user)
#     return result
