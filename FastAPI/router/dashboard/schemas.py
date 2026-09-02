from pydantic import BaseModel, computed_field
from typing import List, Dict, Any
import uuid

class DashboardResponse(BaseModel):
    id: uuid.UUID
    name: str
    phone: str
    email: str
    friends: List[Dict[str, Any]]
    in_grp: List[Dict[str, Any]]
    exp_frnd: List[Dict[str, Any]]
    tot_owe: int
    tot_lend: int
    created_at: str

    @computed_field
    def net_balance(self) -> int:
        return self.tot_lend - self.tot_owe

class UpdateProfileRequest(BaseModel):
    display_name: str
    phone: str

class GroupResponse(BaseModel):
    id: uuid.UUID
    name: str
    members: List[Dict[str, Any]]
    created_at: str
    created_by: uuid.UUID
    created_by_name: str = ""
