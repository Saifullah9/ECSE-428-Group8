from db.mongo import MongoSession
from fastapi_users import FastAPIUsers
from fastapi_users.db import MongoDBUserDatabase
from model.user import User, UserCreate, UserDB, UserUpdate

from api.config import jwt_authentication

# Database for users
mongo_db_users = MongoSession(collection='users')
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
