from typing import List, Optional
from fastapi import status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db
from ..utils import hash_password
from ..models import User
from sqlalchemy import func

router = APIRouter(
    prefix="/v1/users",
    tags=["Users"]
)


@router.get("/", response_model=schemas.UserOutWithPagination)
def get_users(limit: Optional[int] = 10, skip: Optional[int] = 0, search: Optional[str] = "", 
              sort: Optional[str] = "id", order: Optional[str] = "desc",
              db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    users = db.query(models.User)
    if search:
         users = users.filter(models.User.email.contains(search))
    if limit:
        users = users.limit(limit).offset(skip)
    users = users.add_columns(func.count().over().label('total')).all()
    total = users[0][-1] if len(users) else 0
    
    return {'data': map(lambda user : user[0], users), 'total':total}


@router.get("/{user_id}", response_model=schemas.User)
def get_user(user_id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    user = db.query(models.User).filter(models.User.id == user_id).first()
    check_if_exists(user, user_id)
    return user


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    hashed_password = hash_password(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def check_if_exists(user, user_id):
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with {user_id} id was not found")