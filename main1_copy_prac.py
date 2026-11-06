from fastapi import FastAPI,HTTPException,Path
from fastapi.responses import JSONResponse
from pydantic import BaseModel,Field,computed_field
from typing import Annotated,Literal,Optional
import json

app = FastAPI()

class patient(BaseModel):

    id : Annotated[str,Field(...,description="Enter the patient id",examples=["P001"])]
    name : Annotated[str,Field(...,description='patient name',max_length=50,min_length=0)]
    city : Annotated[str,Field(...,description='city where patient lives')]
    age : Annotated[int,Field(...,description='patient age',gt = 0)]
    gender : Annotated[Literal['male','female','other'],Field(...,description='patient gender')]
    height : Annotated[float,Field(...,description='patient height',gt = 0)]
    weight : Annotated[float,Field(...,description='patient height',gt = 0)]


    @computed_field
    @property
    def BMI(self) -> float:
        bmi = round((self.weight/self.height**2),2)
        return bmi

    @computed_field
    @property
    def verdict(self)->str:
        if self.BMI < 18.5:
            return 'underweight'
        elif self.BMI < 25:
            return 'Normal'
        elif self.BMI < 30:
            return 'Overwight'
        else:
            return 'obese'

class patientUpdate(BaseModel):

    name : Annotated[Optional[str],Field(default=None)]
    city : Annotated[Optional[str],Field(default=None)]
    age : Annotated[Optional[int],Field(default=None,gt=0)]
    gender : Annotated[Optional[Literal['male','female','other']],Field(default=None)]
    height : Annotated[Optional[float],Field(default=None,gt=0)]
    weight : Annotated[Optional[float],Field(default=None,gt = 0)]

        
def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
        return data

def save_data(data):
    with open("patient.json","w") as f:
        json.dump(data,f,indent=4)

@app.get("/view")
def view():
    data = load_data()

    return data



@app.get("/patient/{patient_id}")
def patient_data(patient_id : str = Path(...,description="Enter the patient ID",examples=["P001"]) ):
    data = load_data()

    if patient_id in data:
        return data[patient_id]
    raise HTTPException(status_code=404, detail="error found!")

@app.post("/creates")
def add_details(patients : patient):

    data = load_data()

    if patients.id in data:
        raise HTTPException(status_code=400, detail="Patient already exist in the database")

    data[patients.id] = patients.model_dump(exclude={'id'})

    save_data(data)

    return JSONResponse(status_code=201, content={"message":"patient created successfully!"})

patient_info = {'id':'P002','name' : 'abhay vishwakarma','city':'bhadohi','age':40,'gender':'male','height':181.4,'weight':400.9}


patient1 = patient(**patient_info) 

def insert_patient_data(patient1 : patient):
    print(patient1.id)
    print(patient1.name)
    print(patient1.city)
    print(patient1.age)
    print(patient1.gender)
    print(patient1.height)
    print(patient1.weight)
    print(patient1.BMI)
    print(patient1.verdict)

#insert_patient_data(patient1)

@app.put('/edit{patient_id}')
def update_patient(patient_id : str,request_body : patientUpdate):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404 , detail='patient not found')
    existing_patient_info = data[patient_id]

    updated_patient_info =   request_body.model_dump(exclude_unset=True)

    for key,value in updated_patient_info.items():
        existing_patient_info[key] = value

    existing_patient_info['id'] = patient_id

    patient_pydantic_obj = patient(**existing_patient_info)

    existing_patient_info= patient_pydantic_obj.model_dump(exclude='id')

    data[patient_id] = existing_patient_info

    save_data(data)
    return JSONResponse(status_code=200, content='patient updated')

@app.delete('/delete/{patients_id}')
def delete_patient(patients_id : str):

    data = load_data()

    if patients_id not in data:
        raise HTTPException(status_code=404 , detail='patient not found')

    del data[patients_id] 

    save_data(data)

    return JSONResponse(status_code=200,content={'message':'patient info deleted!'})
   