from fastapi import Depends, status, HTTPException
from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas
from fastapi.security import OAuth2PasswordBearer


oauth2_scheme = OAuth2PasswordBearer('login')

#SECRET_KEY
SECRET_KEY = "DhUw6VcpFpQ5PclHLyJtZ+9hHzzOrUVeY1Gho0qGQkUjJ5cs9zhszzSJT8QK6rED"
#ALGORITHM
ALGORITHM = "HS256"
#EXPIRATION TIME IN MINUTES
ACCESS_TOKEN_EXPIRE_TIME = 30

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
    
def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail=f"Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    return verify_access_token(token=token, credential_exceptions=credentials_exception)