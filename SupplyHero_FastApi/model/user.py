from fastapi_users.models import BaseUser, BaseUserCreate, BaseUserDB, BaseUserUpdate


class User(BaseUser):
    pass

class UserCreate(BaseUserCreate):
    pass

class UserUpdate(User, BaseUserUpdate):
    pass

class UserDB(User, BaseUserDB):
    pass
