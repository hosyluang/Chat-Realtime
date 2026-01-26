from pydantic import BaseModel
from datetime import datetime
from app.schemas.user import UserResponse


class FriendRequestCreate(BaseModel):
    receiver_id: int


class FriendshipResponse(BaseModel):
    id: int
    sender_id: int
    receiver_id: int
    status: str
    created_at: datetime
    sender: UserResponse
    receiver: UserResponse

    class Config:
        from_attributes = True
