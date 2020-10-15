from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

from model.student import Student

class User(BaseModel):
    fullname: str
    username: str
    email: EmailStr
    password: str
    students: List[Student]