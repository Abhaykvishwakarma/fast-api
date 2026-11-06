from fastapi import FastAPI,Path,HTTPException , Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated , Literal
import json

app = FastAPI()

class Patient(BaseModel):

    id : Annotated[str,Field(...,description='ID of the patient',examples=['P001'])]
    name : Annotated[str,Field(...,description='Name of the patient')]
    city : Annotated[str,Field(...,description='patient current city where he lives')]
    gender:Annotated[Literal['male','female','other'],Field(...,description='gender of the patient')]
    age:Annotated[int,Field(...,gt=0,description='patient age')]
    height : Annotated[float,Field(...,gt=0,description='patient hight in meter')]
    weight : Annotated[float,Field(...,gt=0,description='patient weight in kg')]

    @computed_field
    @property
    def bMi(self)->float:
        bmi = round((self.weight/self.height),2)
        return bmi

    @computed_field
    @property
    def vedict(self)->str:
        if self.bMi < 18.5:
            return 'underweight'
        elif self.bMi < 25:
            return 'Normal'
        elif self.bMi < 30:
            return 'Overwight'
        else:
            return 'obese'



@app.get("/")
def hello():
    return {'message' : 'patient management system'}

def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data ,f,indent=4)


@app.get("/about")
def about():
    return {'message' : 'A fully functional API to manage your patient records'}


@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patient(patient_id:str = Path(..., description = "ID of the patient in the DB",examples='P001')):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    else:
        raise HTTPException(status_code = 404, detail = "patient not found")

    
@app.get("/sort")
def sort_patients(sort_by : str = Query(..., description='sort on the basis of height, weight or bmi'), order: str = Query('asc',description='sort in asc or desc order')):

    valid_feilds = ['height','weight','bmi']

    if sort_by not in valid_feilds:
        raise HTTPException(status_code= 400,detail=f'Invalid field select from {valid_feilds}')
    if order not in ['asc','desc']:
        raise HTTPException(status_code = 400, detail= 'Invalid select order from asc or desc')
    

    data = load_data()

    sorted_order = True if order == 'desc' else False
    
    sorted_data = sorted(data.values(),key = lambda x : x.get(sort_by,0),reverse = sorted_order)

    return sorted_data

@app.post('/create')
def create_patient(patient1 : Patient):

    data = load_data()

    if patient1.id in data:
        return HTTPException(status_code=400 , detail='content is already exits in the database')
    
    data[patient1.id] = patient1.model_dump(exclude=['id'])
    save_data(data)

    return JSONResponse(status_code=201,content={'message':'patient created successfully'})