from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange
import psycopg
import time

app=FastAPI()

## Validating Schema
class Post(BaseModel):
    title: str
    content: str 
    published: bool = True

### Postrgres Connection psycopg
try:
    with psycopg.connect(host='localhost',
    dbname='fastapi',
    user='postgres',
    password='May@1425',
    row_factory=psycopg.rows.dict_row) as conn:
        with conn.cursor() as cursor:
            print("Database connection was successfull")
except Exception as error:
        print("Connecting to Database Failed")
        print("Error: ", error)
        time.sleep(2)


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
def get_posts():
    return {"data": my_posts}

## Read with id
@app.get("/posts/{id}")
def get_post(id:int,response:Response):

    post=find_post(id)
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
def validated_post(new_post: Post):
    post_dict = new_post.model_dump()
    post_dict['id']=randrange(0,1000)
    my_posts.append(post_dict)
    return {"data":post_dict}
# title str, content str 

## Create Post By ID

@app.post('/createposts')
def create_post(payload: dict = Body(...)):
    print(payload)
    return {"new_post":f"title {payload['title']} content: {payload['content']}"}

## Delete

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # Delete post
    # find the index in the array using custom function
    # my_post.pop(index)
    index=find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    my_posts.pop(index)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## Update 

@app.put("/posts/{id}")
def update_post(id:int,post: Post):
    index = find_post_index(id)
    if index == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    post_dict = post.model_dump()
    post_dict['id'] = id
    my_posts[index] = post_dict
    return {"data":post_dict}
