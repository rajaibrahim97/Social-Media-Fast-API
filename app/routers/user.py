
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter
from .. import models, schemas
from ..database import get_db
from .. import utils
from sqlalchemy.orm import Session

router=APIRouter(
    prefix="/users",
    tags=['Users']
)

### Create User
#response_model=schemas.PostResponse
@router.post('/',status_code=status.HTTP_201_CREATED)
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
@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int,db:Session=Depends(get_db)):
    user_info=db.query(models.User).filter(models.User.id==id).first()
    if not user_info:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with {id} not found.')
    return user_info