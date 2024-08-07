from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .. import models, schemas, oauth2
from ..database import get_db
from ..models import User

router = APIRouter(
    prefix="/v1/posts",
    tags=["Posts"]
)


@router.get("/", response_model=schemas.PostOutWithPagination)
def get_posts(limit: Optional[int] = 10, skip: Optional[int] = 0, owner_id: Optional[int] = 0, search: Optional[str] = "", 
              sort: Optional[str] = "id", order: Optional[str] = "desc", db: Session = Depends(get_db),
              current_user: User = Depends(oauth2.get_current_user)):
    data = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                         models.Vote.post_id == models.Post.id,
                                                                                         isouter=True).group_by(
        models.Post.id)
    if search:
        data = data.filter(models.Post.title.contains(search)| models.Post.content.contains(search))
    if owner_id:
        data = data.filter(models.Post.owner_id == owner_id)    
        
    data = data.order_by(text(f'{sort} {order}'))
    if limit:
        data = data.limit(limit).offset(skip)
    data = data.add_columns(func.count().over().label('total')).all()
    total = data[0][-1] if len(data) else 0
    return {'data': data, 'total':total}


@router.get("/{post_id}", response_model=schemas.PostOut)
def get_post(post_id: int, db: Session = Depends(get_db), current_user: User = Depends(oauth2.get_current_user)):
    post = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote,
                                                                                      models.Vote.post_id == models.Post.id,
                                                                                      isouter=True).group_by(
        models.Post.id).filter(models.Post.id == post_id).first()

    check_if_exists(post, post_id)
    return post


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    new_post = models.Post(owner_id=current_user.id, **post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)

    return new_post


@router.put("/{post_id}", response_model=schemas.Post)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    found_post = post_query.first()

    check_if_exists(found_post, post_id)
    if found_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.update(post.dict(), synchronize_session=False)
    db.commit()

    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    check_if_exists(post, post_id)

    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    post_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def check_if_exists(post, post_id):
    if post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Post with {post_id} id was not found")

