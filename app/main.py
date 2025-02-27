from fastapi import FastAPI
from random import randrange
from .config import settings
### SQLALCHEMY 
from . import models
from .database import engine
from app.routers import router
from fastapi.middleware.cors import CORSMiddleware

### Initiating DB
#models.Base.metadata.create_all(bind=engine)

app=FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
app.include_router(router)

@app.get("/")
def root():
    return {"message":"Welcome to my api"}



    


