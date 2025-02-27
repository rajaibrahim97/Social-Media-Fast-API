
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models, schemas,oauth2
from ..database import get_db
from sqlalchemy.orm import Session
from typing import Optional,List
from random import randrange
from fastapi.params import Body
from sqlalchemy import func


router=APIRouter(
    prefix="/posts",
      tags=['Posts']
)

## Read
# ,response_model=List[schemas.PostVote]
@router.get('/',response_model=List[schemas.PostVote])
def get_posts(db=Depends(get_db),current_user:int = Depends(oauth2.get_current_userr),limit: int = 10,skip: int = 0, search: Optional[str] = ""):
    #posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    posts = db.query(models.Post,
                       func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts
## Read with id
@router.get("/{id}",response_model=schemas.PostVote)
def get_post(id:int,response:Response,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_userr)):

    post = db.query(models.Post,
                       func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id==models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id)\
        .first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} was not found")
        #response.status_code = status.HTTP_404_NOT_FOUND
        #return {"message":f"post with id: {id} was not found"}
    return post

 
### Create Raw without schema example
#@router.post('/createposts')
#def create_post(payload: dict = Body(...)):
   # print(payload)
   # return {"new_post":f"title {payload['title']} content: {payload['content']}"}


## Create

### schema pydantic --> title: str, content: str
@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def validated_post(new_post: schemas.PostCreate,db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_userr)):
    posts=models.Post(owner_id=current_user.id,**new_post.model_dump())
    db.add(posts)
    db.commit()
    db.refresh(posts)
    return posts
# title str, content str 

## Create Post By ID

## Delete

@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_userr)):
    delete_query=db.query(models.Post).filter(models.Post.id==id)
    post=delete_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")
    
    delete_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


## Update 

@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,new_post: schemas.PostCreate,db:Session=Depends(get_db),current_user:int = Depends(oauth2.get_current_userr)):
    #db.execute("""update posts set title =%s, content=%s,published=%s where id=%s returning*""",(post.title,post.content,post.published,str(id)))
    #updated_post=db.fetchone()
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post = post_query.first()
    if post is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {id} does not exist")
    
    if post.owner_id != current_user.id:
         raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    post_query.update(new_post.model_dump(),synchronize_session=False)
    updated_post=post_query.first()
    db.commit()
    db.refresh(updated_post)

    return updated_post

