## Validating Schema
from pydantic import BaseModel,EmailStr,Field
from datetime import datetime
from typing import Optional




## User
class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at: datetime
    class Config:
        from_attributes=True


class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        from_attributes=True


class TokenData(BaseModel):
    id : Optional[str]=None
## Post
class PostBase(BaseModel):
    title: str
    content: str 
    published: bool = True

class PostCreate(PostBase):
    pass

class PostResponse(PostBase):
    id:int
    created_at: datetime
    owner_id: int
    owner: UserOut
    class Config:
        from_attributes=True


class PostVote(BaseModel):
    Post:PostResponse
    votes: int
    class Config:
        from_attributes=True

## Auth

class UserLogin(BaseModel):
    email:EmailStr
    password: str
    #created_at:datetime
    class Config:
        from_attributes=True

class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id : Optional[str]=None


## Vote 
class Vote(BaseModel):
    post_id : int 
    # user_id is not needed as it is going to be provided by JWT
    dir: int = Field(..., ge=0, le=1)
