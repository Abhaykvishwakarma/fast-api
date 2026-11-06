from pydantic import BaseModel

class address(BaseModel):

    city : str
    state : str
    pincode : int

class patient(BaseModel):

    name :str
    age:int
    gender:str
    Address : address

dict_address = {'city':'bhadohi','state':'uttar pradesh','pincode':221401}

address1 = address(**dict_address)

patient_dict = {'name':'amritesh pandey','age':22,'gender':'male','Address':address1}

patient1 = patient(**patient_dict)
print(patient1)