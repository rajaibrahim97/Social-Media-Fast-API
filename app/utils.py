from passlib.context import CryptContext
pwd_context=CryptContext(schemes=["bcrypt"])

## password hashing 
def hash(password:str):
    return pwd_context.hash(password)

## Auth hash verification used in auth.py
def verify(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)
    

