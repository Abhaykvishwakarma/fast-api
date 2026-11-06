from fastapi import FastAPI,Path,HTTPException , Query
from pydantic import BaseModel,Field,computed_field
from fastapi.responses import JSONResponse
from typing import Annotated , Literal,Optional
import json

app = FastAPI()

class patient(BaseModel):

    id : Annotated[str,Field(...,description='id of the patient',examples=['P001'])]
    name : Annotated[str,Field(...,description='name of the patient',)]
    city : Annotated[str,Field(...,description='city name where the paitient lives')]
    age : Annotated[int,Field(...,description='age of the patient')]
    height : Annotated[float,Field(...,description='height of the patient')]
    weight : Annotated[float,Field(...,description='weight of the patient')]

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

class patient_update(BaseModel):

    name : Annotated[Optional[str],Field(default=None)]
    city : Annotated[Optional[str],Field(default=None)]
    age : Annotated[Optional[int],Field(default=None,gt=0)]
    height:Annotated[Optional[float],Field(default=None,gt=0)]
    weight : Annotated[Optional[float],Field(default=None,gt=0)]


def load_data():
    with open('patient.json','r') as f:
        data = json.load(f)
        return data
    
def save_data(data):
    with open('patient.json','w') as f:
        json.dump(data,f,indent=4)

@app.put('/edit/{patient_id}')
def update_patient(patient_id:str , patientupdate:patient_update):

    data = load_data()

    if patient_id not in data:
        raise HTTPException(status_code=404,detail='patient not found')

    existing_data_info = data[patient_id]

    patientupdate.model_dump(exclude_unset=True)

    for key,value in patientupdate.items():
        existing_data_info[key] = value

    existing_data_info['id'] = patient_id
    patient(**existing_data_info)

    data[patient_id] = existing_data_info

    save_data(data)

    return JSONResponse(status_code=200 , content={'message':'patient detail updated!'})


    
    
    