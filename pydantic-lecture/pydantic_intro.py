
from pydantic import BaseModel,EmailStr,AnyUrl
from typing import List,Dict,Optional


class Patient(BaseModel):

    name : str
    age : int
    id : Optional[float] = None
    gender:str
    hobbies: List[str]
    address: Dict[str , str]
    email : EmailStr
    linkdin : AnyUrl

def insert_patient_data(patient1 : Patient):
    print(patient1.name)
    print(patient1.age)
    print(patient1.id)
    print(patient1.hobbies)
    print(patient1.gender)
    print(patient1.address)
    print(patient1.email)
    print(patient1.linkdin)
    print("inserted in database")



patient_data = {'name' : 'abhay vishwakarma','age' : '33','id':200.1,'hobbies':['cricket','chess','playing onine games like ff','talking with friends','study','explring new things'],
                'gender':'male','address':{'email':'Abhay@gmail.com','mobile no.':'48493238439'},'email':'Ajay@gmail.com','linkdin':'http://linkedin.com/2345'}

patient1 = Patient(**patient_data)      

insert_patient_data(patient1)