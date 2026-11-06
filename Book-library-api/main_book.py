from fastapi import FastAPI
from pydantic import BaseModel,Field
from typing import Optional,Annotated


app = FastAPI()

class Books(BaseModel):

    title : str
    author : str
    id : int
    genre : str = 'fiction'
    isbn : Optional[str] = None
    rating : Annotated[int,Field(gt = 0,le = 10)]

data = [{'title':'this book is based on human pyscology','author':'brettlee','id':1},{'title':'make life better','author':'santuklam alii','id':2},{'title':'become more dangerous','author':'james bond','id':3}]

@app.get('/books')
def get_books():
    return {'data':data}

@app.post('/book')
def create_entry(book : Books):
    print(type(book))
    item_dict = book.model_dump()
    data.append(item_dict)
    return {"message" : "success"}

@app.get('/book/{id}')
def get_book(id : int):

    for p in data:
        if p['id'] == id:
            return {'id_data' : p}
    return {'message':'id not found!'}