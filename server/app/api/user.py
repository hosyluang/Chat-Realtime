from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import UserResponse

router = APIRouter(prefix="/users", tags=["Users"])


# api lay thong tin ban than
@router.get("/me", response_model=UserResponse)
def read_user_me(current_user: User = Depends(get_current_user)):
    return current_user


# api tim kiem user khac
@router.get("/search", response_model=List[UserResponse])
def search_user(
    q: str,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    users = (
        db.query(User)
        .filter(
            (User.username.ilike(f"%{q}%")) | (User.email.ilike(f"%{q}%")),
            User.id != current_user.id,
        )
        .all()
    )

    return users
