from jose import JWTError,jwt
from datetime import datetime,timedelta,timezone
from ..import schemas,database,models
from fastapi import Depends,HTTPException,status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import session
from..config import setting

oauth2_scheme = OAuth2PasswordBearer(tokenUrl='login')

SECREY_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes

def create_access_token(data : dict):

    to_encode = data.copy()

    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":expire})

    encoded_jwt = jwt.encode(to_encode,SECREY_KEY,algorithm=ALGORITHM)

    return encoded_jwt

def verify_access_token(Token:str,credentials_exception):

    try:
        payload = jwt.decode(Token,SECREY_KEY,algorithms=[ALGORITHM])

        id:str = payload.get("user_id")
        email = payload.get("email")

        if id is None:
            raise credentials_exception
        Token_data = schemas.TokenData(id=id,email=email)
    except JWTError:
        raise credentials_exception 

    return Token_data

def get_current_user(token:str = Depends(oauth2_scheme),db:session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=401,detail=f"could not valid credentials",headers={"WWW-Authenticate":"Bearer"})

    Token = verify_access_token(token,credentials_exception)

    user = db.query(models.User).filter(models.User.id == Token.id).first()

    return user
    

