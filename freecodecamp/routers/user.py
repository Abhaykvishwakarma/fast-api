from fastapi import FastAPI,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import utils,schemas,models
from ..database import get_db

router = APIRouter(
    prefix="/users",
    tags=['users']
)

@router.post("/",status_code=201,response_model=schemas.userout)
def users(user : schemas.User,db:Session = Depends(get_db)):

    hashed_password = utils.hash(user.password)
    user.password = hashed_password

    new_user = models.User(**user.model_dump())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

@router.get("/{id}",response_model=schemas.userout)
def get_user(id :int,db:Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.id == id).first()

    if user == None:
        raise HTTPException(status_code=404 ,detail=f"id {id} no data found")

    return user
