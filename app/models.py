from sqlalchemy import Column, Integer, String, Boolean, text, TIMESTAMP, ForeignKey
from sqlalchemy.orm import relationship
from .database import Base
from sqlalchemy.sql import expression

class EntityBase:
    id = Column(Integer, primary_key=True, nullable=False, autoincrement=True)
    created_at = Column(TIMESTAMP(timezone=True), nullable=False, server_default=text("now()"))
    updated_at = Column(TIMESTAMP(timezone=True), nullable=True, server_default=text("CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP"))


class Post(Base, EntityBase):
    __tablename__ = "posts"

    title = Column(String(200), nullable=False)
    content = Column(String(500), nullable=False)
    published = Column(Boolean, nullable=False, server_default=expression.true())
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")


class User(Base, EntityBase):
    __tablename__ = "users"

    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    avatar = Column(String(200), nullable=False)


class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), primary_key=True, nullable=False)
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), primary_key=True, nullable=False)

class Comment(Base, EntityBase):
    __tablename__ = "comments"
    
    content = Column(String(500), nullable=False)
    owner_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    owner = relationship("User")
    post_id = Column(Integer, ForeignKey("posts.id", ondelete="CASCADE"), nullable=False)
    edited = Column(Boolean, nullable=False, server_default=expression.false())