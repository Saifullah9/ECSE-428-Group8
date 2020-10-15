from typing import Optional, List
from pydantic import BaseModel, EmailStr, Field

class Student(BaseModel):
    fullname: str
    school_name: str
    school_supplies: List[str]