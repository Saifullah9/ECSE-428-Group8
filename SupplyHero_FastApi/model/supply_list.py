from typing import List
from uuid import UUID
from fastapi import FastAPI
from pydantic import BaseModel

class SupplyList(BaseModel):
    old_id: UUID
    list_of_supplies: List[str]
      
class SupplyListPrivilege(BaseModel):
    email: str 
    privilege_type: str
    supply_list_id: UUID