from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional,List
from random import randrange
import psycopg
from psycopg_pool import ConnectionPool
import time
from. import utils
### SQLALCHEMY 
from . import models, schemas
from .database import engine,get_db
from sqlalchemy.orm import Session
from app.models import Base



models.Base.metadata.create_all(bind=engine)

app=FastAPI()



# Create the connection pool
pool = ConnectionPool(
    conninfo="host=localhost dbname=fastapi user=postgres password=May@1425",
    min_size=2,
    max_size=10
)
## Dummy Database
my_posts = [{"title":"title 1 of post 1","content":"content of post 1","id":1},
            {"title":"Favorite Food", "content":"I like pizza","id":2}]


def find_post(id):
    for p in my_posts:
        if p["id"]==id:
            return p 
        
def find_post_index(id):
    for i,p in enumerate(my_posts):
        if p["id"]==id:
            return i


# CRUD Operation

### READ

@app.get("/")
def root():
    return {"message":"Welcome to my api"}


@app.get('/posts',response_model=List[schemas.PostResponse])
def get_posts(db=Depends(get_db)):
    
    posts=db.query(models.Post).all()
    return  posts
## Read with id
@app.get("/posts/{id}")
def get_post(id:int,response:Response,db:Session = Depends(get_db)):

    post=db.query(models.Post).filter(models.Post.id==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id: {id} was not found"}
    return post


### Create Raw without schema example
@app.post('/createposts')
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title {payload['title']} content: {payload['content']}"}


## Create

### schema pydantic --> title: str, content: str
@app.post('/posts',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def validated_post(new_post: schemas.PostCreate,db:Session = Depends(get_db)):
    posts=models.Post(**new_post.model_dump())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts
# title str, content str 

## Create Post By ID

@app.post('/createposts')
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title {payload['title']} content: {payload['content']}"}

## Delete

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    delete_query=db.query(models.Post).filter(models.Post.id==id)
    post=delete_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## Update 

@app.put("/posts/{id}",response_model=schemas.PostResponse)
def update_post(id:int,new_post: schemas.PostCreate,db:Session=Depends(get_db)):
    #db.execute("""update posts set title =%s, content=%s,published=%s where id=%s returning*""",(post.title,post.content,post.published,str(id)))
    #updated_post=db.fetchone()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    post_query.update(new_post.model_dump(),synchronize_session=False)
    updated_post=post_query.first()
    db.commit()
    db.refresh(updated_post)

    return updated_post
    
### Create User
#response_model=schemas.PostResponse
@app.post('/users',status_code=status.HTTP_201_CREATED)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    # hash the password
    hash_password=utils.hash(user.password)
    user.password=hash_password

    new_user=models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

## Get User
@app.get("/user/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user_info=db.query(models.User).filter(models.User.id==id).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with {id} not found.')
    return user_info

