from fastapi import APIRouter, Depends, HTTPException, status
from typing import List
from sqlalchemy import or_, and_
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.models.friendship import Friendship
from app.schemas.friend import FriendRequestCreate, FriendshipResponse

router = APIRouter(prefix="/friends", tags=["Friends"])


# gui loi moi ket ban
@router.post("/request", response_model=FriendshipResponse)
def send_friend_request(
    request_data: FriendRequestCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # ko duoc ket ban chinh minh
    if request_data.receiver_id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Cannot send friend request to yourself",
        )
    # kiem tra xem moi quan he da ton tai chua
    existing_friendship = (
        db.query(Friendship)
        .filter(
            or_(
                and_(
                    Friendship.sender_id == current_user.id,
                    Friendship.receiver_id == request_data.receiver_id,
                ),
                and_(
                    Friendship.sender_id == request_data.receiver_id,
                    Friendship.receiver_id == current_user.id,
                ),
            )
        )
        .first()
    )
    if existing_friendship:
        if existing_friendship.status == "PENDING":
            raise HTTPException(status_code=400, detail="Friend request already sent")
        if existing_friendship.status == "ACCEPTED":
            raise HTTPException(status_code=400, detail="You are already friends")
    # tao loi moi
    new_friendship = Friendship(
        sender_id=current_user.id,
        receiver_id=request_data.receiver_id,
        status="PENDING",
    )
    db.add(new_friendship)
    db.commit()
    db.refresh(new_friendship)
    return new_friendship


@router.post("/accept/{friendship_id}")
def accept_friend_request(
    friendship_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    # tim loi moi
    friendship = db.query(Friendship).filter(Friendship.id == friendship_id).first()
    if not friendship:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Friend request not found"
        )
    # chi nguoi nhan moi dc chap nhan
    if friendship.receiver_id != current_user.id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="You are not authorized to accept this request",
        )
    friendship.status = "ACCEPTED"
    db.commit()
    return {"msg": "Friend request accepted"}


@router.get("/", response_model=List[FriendshipResponse])
def get_friend(
    db: Session = Depends(get_db), current_user: User = Depends(get_current_user)
):
    # Lay tat ca quan he ma minh la nguoi sender va receiver, status la accept
    friends = (
        db.query(Friendship)
        .join(
            User,
            or_(User.id == Friendship.sender_id, User.id == Friendship.receiver_id),
        )
        .filter(
            Friendship.status == "ACCEPTED",
            or_(
                Friendship.sender_id == current_user.id,
                Friendship.receiver_id == current_user.id,
            ),
        )
        .all()
    )

    return friends
