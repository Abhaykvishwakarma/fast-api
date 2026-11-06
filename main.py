from fastapi import FastAPI

app = FastAPI()

@app.get("/abhay")
def Hello():
    return "{message : Hello world} "

@app.get("/aboutme")
def about():
    return "{message} : {i am the best}"