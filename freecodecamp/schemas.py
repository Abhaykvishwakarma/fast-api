from pydantic import BaseModel,EmailStr
from datetime import datetime
from typing import Optional

class PostBase(BaseModel):

    title:str
    content:str
    published:bool = True

class createPost(PostBase):
    pass

class updatePost(PostBase): 
    pass

class userout(BaseModel):
    email : EmailStr
    id:int
    created_at: datetime
    
    class config:
        orm_mode = True

class Post(PostBase):
    id:int
    created_at: datetime
    owner_id : int
    owner : userout

    class config:
        orm_mode = True


class User(BaseModel):

    email:EmailStr
    password:str



class loginUser(BaseModel):
    email : EmailStr
    password : str


class Token(BaseModel):
    access_token : str
    token_type : str

    

class TokenData(BaseModel):
    id: Optional[int] = None
    email:Optional[EmailStr] = None
    