from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
from psycopg_pool import ConnectionPool


import time

app=FastAPI()

## Validating Schema
class Post(BaseModel):
    title: str
    content: str 
    published: bool = True


# Create the connection pool
pool = ConnectionPool(
    conninfo="host=localhost dbname=fastapi user=postgres password=May@1425",
    min_size=2,
    max_size=10
)
## Database Connection with psycorg Function
def get_db():
    try:
        with pool.connection() as conn:  # Use `with` to handle connection cleanup
            with conn.cursor(row_factory=psycopg.rows.dict_row) as cur:
                yield cur  # Yield cursor for FastAPI dependency
                conn.commit()  # Commit transaction after usage
    except psycopg.Error as error:
        print("Database connection failed:", error)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Database connection failed")

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

## Read 
@app.get("/")
def root():
    return {"message":"Welcome to my api"}

@app.get('/posts')
def get_posts(db=Depends(get_db)):
    db.execute("SELECT * FROM posts")
    posts=db.fetchall()
    return {"data": posts}
## Read with id
@app.get("/posts/{id}")
def get_post(id:int,response:Response,db=Depends(get_db)):
    db.execute("""select * from posts where id = %s""",(str(id),))
    post=db.fetchone()
    print(post)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id: {id} was not found"}
    return {"post_detail":post}
@app.post('/createposts')
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title {payload['title']} content: {payload['content']}"}


## Create

### schema pydantic --> title: str, content: str
@app.post('/posts',status_code=status.HTTP_201_CREATED)
def validated_post(new_post: Post,db=Depends(get_db)):
    print(new_post)
    db.execute("""insert into posts (title,content,published) values (%s,%s,%s) returning *""",
               (new_post.title,new_post.content,new_post.published))
    post=db.fetchone()
    return {"data":post}
# title str, content str 

## Create Post By ID

@app.post('/createposts')
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title {payload['title']} content: {payload['content']}"}

## Delete

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db=Depends(get_db)):
    # Delete post
    # find the index in the array using custom function
    # my_post.pop(index)
    db.execute("""delete from posts where id=%s returning*""",(str(id),))
    deleted_post=db.fetchone()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## Update 

@app.put("/posts/{id}")
def update_post(id:int,post: Post,db=Depends(get_db)):
    db.execute("""update posts set title =%s, content=%s,published=%s where id=%s returning*""",(post.title,post.content,post.published,str(id)))
    updated_post=db.fetchone()
    if updated_post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    return {"data":updated_post}
    
