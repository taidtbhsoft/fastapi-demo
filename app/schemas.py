from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, Field
from pydantic.types import conint


class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length = 6)


class User(BaseModel):
    id: int
    email: str
    avatar: str
    created_at: datetime

    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True


class PostCreate(PostBase):
    pass


class Post(PostBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    owner: User

    class Config:
        from_attributes = True


class PostOut(BaseModel):
    Post: Post
    votes: int
    comments: int

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    id: Optional[str]
    username: Optional[str]


class Vote(BaseModel):
    post_id: int
    direction: conint(le=1)

class PostOutWithPagination(BaseModel):
    data: list[PostOut] = []
    total: int

    class Config:
        from_attributes = True

class UserOutWithPagination(BaseModel):
    data: list[User] = []
    total: int

    class Config:
        from_attributes = True
# Comments
class CommentBase(BaseModel):
    post_id: int
    content: str

class Comment(CommentBase):
    id: int
    created_at: datetime
    updated_at: datetime
    owner_id: int
    edited: bool = True
    owner: User

    class Config:
        from_attributes = True

class CommentCreate(CommentBase):
    pass

class CommentUpdate(BaseModel):
    content: str

class CommentOutWithPagination(BaseModel):
    data: list[Comment] = []
    total: int

    class Config:
        from_attributes = True