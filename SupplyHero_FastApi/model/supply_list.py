from pydantic import BaseModel
from uuid import UUID

class SupplyListPrivilege(BaseModel):
    email: str 
    privilege_type: str
    supply_list_id: UUID