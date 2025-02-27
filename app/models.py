#from .database import Base
from sqlalchemy import Column, Integer, String,Boolean,ForeignKey
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.sql.sqltypes import TIMESTAMP
from sqlalchemy.sql.expression import text
from sqlalchemy.orm import relationship

Base=declarative_base()

class Post(Base):
    __tablename__="posts"
    
    id = Column(Integer, primary_key=True, nullable=False)  # Unique ID
    title = Column(String, nullable=False)  # Title column (string)
    content = Column(String, nullable=False)  # Content column (string)
    published = Column(Boolean, server_default='TRUE',nullable=False)  # Boolean column with default value
    created_at = Column(TIMESTAMP(timezone=True),nullable=False,server_default=text("now()"))
    owner_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),nullable=False)
    owner = relationship("User")

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,nullable=False)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False,unique=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('now()'))



class Vote(Base):
    __tablename__ = "votes"
    user_id = Column(Integer,ForeignKey("users.id",ondelete="CASCADE"),primary_key=True)
    post_id = Column(Integer,ForeignKey("posts.id",ondelete="CASCADE"),primary_key=True)
    
