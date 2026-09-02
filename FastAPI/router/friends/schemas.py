from pydantic import BaseModel
from uuid import UUID
from typing import Optional


class create_Remove_Friend(BaseModel):
    user_uid: UUID

    friend_name: Optional[str] = None
    friend_email: Optional[str] = None
