from fastapi import FastAPI, Path,HTTPException , Query

import json

app = FastAPI()
def load_data():
    with open("patient.json","r") as f:
        data = json.load(f)
        return data

@app.get("/")
def hello():
    return {'message' : 'patient management system'}

@app.get("/about")
def about():
    return {'message' : 'A fully functional API to manage your patient records'}

@app.get("/view")
def view():
    data = load_data()
    return data

@app.get("/patient/{patient_id}")
def patient(patient_id:str = Path(..., description = "ID of the patient in the DB",example='P001')):
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