from fastapi import FastAPI
from . import models
from .database import engine
from.routers import post,user,auth
from .config import setting


# pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")  #-->here we are telling passlib, what is the default hashing alogorithm or what hashing algorithm do we want to use? In this case, we want to use bcrypt 

models.Base.metadata.create_all(bind=engine)

app = FastAPI()

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)





