from pydantic import BaseModel
from typing import List,Optional

class patient(BaseModel):

    name : str
    age : int
    weight : float
    allergies : Optional[List[str]] = None


def insert_patient_data(patient1:patient):
    print(patient1.name)
    print(patient1.age)
    print(patient1.weight)
    print(patient1.allergies)

    print("done!")


patient_info = {'name':'abhay vishwakarma','age':20,'weight':55.45}

patient1 = patient(**patient_info)

insert_patient_data(patient1)

