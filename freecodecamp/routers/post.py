from fastapi import FastAPI,HTTPException,Response,Depends,APIRouter
from typing import List ,Optional
from sqlalchemy.orm import Session
from .. import models,schemas
from ..database import get_db
from . import oauth2

router = APIRouter(
    prefix="/posts",
    tags=['posts']
)
@router.get("/all",response_model=List[schemas.Post])
def getalluserinfo(db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user),limit : int = 10,skip : int = 0,search:Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")     yaha dekho toh hamne isko direct sqp query ka use karke kiya but ab ham dirct naii karenge ab ham python me orm ka usek karke hi extract kar lenge
    # posts = cursor.fetchall()
    print("abhay")
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    return posts

@router.get("/",response_model=List[schemas.Post])
def root(db:Session = Depends(get_db),users: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts""")     yaha dekho toh hamne isko direct sqp query ka use karke kiya but ab ham dirct naii karenge ab ham python me orm ka usek karke hi extract kar lenge
    # posts = cursor.fetchall()

    posts = db.query(models.Post).filter(models.Post.owner_id == users.id).all()
    return posts


@router.post("/",status_code=201,response_model=schemas.Post)
def create_post(posts:schemas.createPost,db:Session = Depends(get_db),current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,(posts.title,posts.content,posts.published))
    # new_posts = cursor.fetchone()

    # conn.commit()
    print(current_user.id,current_user.email,current_user.created_at)
    new_post = models.Post(owner_id=current_user.id,**posts.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post  #--->dekho isme hamne jo class config karke vo class add kiya hai uska karne ka reason tha ki jab hai usko kiye bina kar rahe the tab na tak error aa raha tha ki jo value return kar rahe haii vo dict type ka  naii hai kyoki aisa karne se vo dict na rahakar sqlalchemy model return kar raha tha phir hamne vo kiya toh vo dict ko ignore karne laga 

@router.get("/{id}",response_model=schemas.Post)
def get_post(id : int,db:Session = Depends(get_db),users: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=404,detail=f"id {id} not found ")
    return post

# @app.get("/sqlalchemy")
# def test_posts(db:Session = Depends(get_db)):

#     posts = db.query(models.Post).all()

#     return {"data" : posts}

@router.delete("/{id}",response_model=schemas.Post)
def delete_post(id : int,db:Session = Depends(get_db),users: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),))
    # deleted_post = cursor.fetchone()
    # print(delete_post)
    # conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code = 404,detail="content not found!")

    if post.owner_id != users.id:
        raise HTTPException(status_code=403,detail="not allowed to delete the post")

    post_query.delete(synchronize_session=False)
    db.commit()
    
    return Response(status_code = 204)

@router.put("/{id}",response_model=schemas.Post)
def update_data(id:int , deleted_post : schemas.updatePost,db:Session = Depends(get_db),users: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,str(id)))

    # updated_post = cursor.fetchone()
    # conn.commit()
    
    post_query = db.query(models.Post).filter(models.Post.id == id)

    post = post_query.first()

    if post is None:
        raise HTTPException(status_code=404,detail=f"id {id} content not found!")

    post_query.update(deleted_post.model_dump(),synchronize_session=False)
    db.commit()

    return  post_query.first()