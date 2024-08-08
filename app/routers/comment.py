from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from sqlalchemy.sql import text
from .. import models, schemas, oauth2
from ..database import get_db
from ..models import User

router = APIRouter(
    prefix="/v1/comment",
    tags=["Comment"]
)

@router.get("/", response_model=schemas.CommentOutWithPagination)
def get_comments(limit: Optional[int] = 10, skip: Optional[int] = 0, owner_id: Optional[int] = 0, 
              search: Optional[str] = "", post_id: int = 0,
              sort: Optional[str] = "id", order: Optional[str] = "desc", db: Session = Depends(get_db),
              current_user: User = Depends(oauth2.get_current_user)):

    data = db.query(models.Comment)
    if search:
        data = data.filter(models.Comment.content.contains(search))
    if owner_id:
        data = data.filter(models.Comment.owner_id == owner_id)    
    if post_id == 0:
        data = data.filter(models.Comment.owner_id == current_user.id)
    else:
        data = data.filter(models.Comment.post_id == post_id)    

        
    data = data.order_by(text(f'{sort} {order}'))
    if limit:
        data = data.limit(limit).offset(skip)
    data = data.add_columns(func.count().over().label('total')).all()
    total = data[0][-1] if len(data) else 0
    return {'data': map(lambda comment : comment[0], data), 'total':total}

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Comment)
def create_comment(comment: schemas.CommentCreate, db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    try:
        new_comment = models.Comment(owner_id=current_user.id, **comment.dict())
        db.add(new_comment)
        db.commit()
        db.refresh(new_comment)
        return new_comment
    except Exception as e:
        print("Error Create Comment")
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Bad request")


@router.put("/{comment_id}", response_model=schemas.Comment)
def update_post(comment_id: int, comment: schemas.CommentUpdate, db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment = comment_query.first()
    check_if_exists(comment, comment_id)
    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")
    comment_query.update({'content': comment.content,'edited': 1}, synchronize_session=False)
    db.commit()

    return comment_query.first()


@router.delete("/{comment_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(comment_id: int, db: Session = Depends(get_db),
                current_user: User = Depends(oauth2.get_current_user)):
    comment_query = db.query(models.Comment).filter(models.Comment.id == comment_id)
    comment = comment_query.first()
    check_if_exists(comment, comment_id)

    if comment.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="Not authorized to perform requested action")

    comment_query.delete(synchronize_session=False)
    db.commit()

    return Response(status_code=status.HTTP_204_NO_CONTENT)


def check_if_exists(comment, comment_id):
    if comment is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Comment with {comment_id} id was not found")
