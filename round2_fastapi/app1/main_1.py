from fastapi import FastAPI,HTTPException,Response,Depends
from fastapi.params import Body
from pydantic import BaseModel
from random import randrange
import psycopg2 
from psycopg2.extras import RealDictCursor
from . import model1
from .database1 import engine,SessionLocal,get_db
from sqlalchemy.orm import Session

model1.Base.metadata.create_all(bind=engine)



app = FastAPI()

class Post(BaseModel):
    title : str
    content : str 
    published : bool = True

try:
    conn = psycopg2.connect(host='localhost',database='fastapi_rev',user='postgres',password='abhay2524',cursor_factory=RealDictCursor)
    cursor = conn.cursor()
    print("database connection successfull")
except Exception as error: 
    print("connecting to database failed!")
    print(f"error : {error}")
    


# post_data = [{"title":"hey this is your abhay","content":"abhay your who is this person this person is super excited for learning the skills which matter for his carrier","id":1},{"title":"today is holiday","content":"today is the day where you all people will understand that i'm the person who is more resposible for the rest of the thing in the world i'm the person who is super motivated and super excited and you guys should understand","id":4},{"title":"playing games","content":"today i was studying with fully focused and try to nutralize my sleep","id":5}]

# def final_post(id):
#     for p in post_data:
#         if p['id'] == id:
#             return p

# def delete_posts(id):
#     for i,p in enumerate(post_data):
#         if p['id'] == id:
#             return i;


@app.get("/")
def get(db:Session = Depends(get_db)):
    posts = db.query(model1.Post).all()
    # cursor.execute("""SELECT * FROM sm_posts""")
    # posts = cursor.fetchall()
    return {"ALL Posts":posts} 


@app.post("/posts")
def post(post : Post):
    
    cursor.execute("""INSERT INTO sm_posts (title,content,published) VALUES(%s,%s,%s) RETURNING *""",(post.title,post.content,post.published))
    new_posts = cursor.fetchone()
    conn.commit()

    
    return {"created post":new_posts}



@app.get("/posts/{id}")
def get_inividual(id:int):

    cursor.execute("""SELECT * FROM sm_posts WHERE id = %s""",str(id))
    posts = cursor.fetchone()
    if posts ==None:
        raise HTTPException(status_code=404,detail=f"id {id} not found!")
    return {"post":posts}



@app.delete("/posts/{id}",status_code=204)
def delete_post(id:int):
    cursor.execute("""delete FROM sm_posts WHERE id = %s RETURNING *""",(id,))
    delete_posts = cursor.fetchone()
    conn.commit()

    if delete_posts == None:
        raise HTTPException(status_code=404,detail=f"id {id} not found!")
   
    
    return Response(status_code=204)


@app.put("/posts/{id}")
def update_post(id:int,post : Post):
    cursor.execute("""update sm_posts SET title = %s, content = %s, published = %s WHERE id = %s RETURNING *""",(post.title,post.content,post.published,id))
    updated_posts = cursor.fetchone()
    conn.commit()
    if updated_posts ==None:
        raise HTTPException(status_code=404,detail="data not found!")
    
    return {"updated posts":updated_posts}