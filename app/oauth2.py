from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta

from . import models, schemas, database
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from .config import settings

oauth2_scheme = OAuth2PasswordBearer('login')

#SECRET_KEY
SECRET_KEY = settings.secret_key
#ALGORITHM
ALGORITHM = settings.algorithm
#EXPIRATION TIME IN MINUTES
ACCESS_TOKEN_EXPIRE_TIME = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_TIME)
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, ALGORITHM)

    return encoded_jwt

def verify_access_token(token: str, credential_exception):
    try:
        payload = jwt.decode(token, SECRET_KEY, [ALGORITHM])
        id: str = payload.get("user_id")

        if id is None:
            raise credential_exception
    
        token_data = schemas.TokenData(id=id)
    except JWTError:
        raise credential_exception
    
    return token_data
    
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(database.get_db)):
    credential_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})

    token = verify_access_token(token, credential_exception)

    user = db.query(models.User).get(token.id)
    return user