from db.mongo import MongoSession, MongoSessionRegular
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from model.user import User, UserCreate, UserDB, UserUpdate
from fastapi import APIRouter, Depends
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

# @router2.post("/reactivate")
# async def reactivate_user(user: User = Depends(fastapi_users.get_current_user)):
#     result = mongo_db_users_reg.reactivate_user(user)
#     return result
