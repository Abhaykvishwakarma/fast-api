from pydantic import BaseModel,Field,EmailStr,field_validator,model_validator
from typing import Annotated,Dict,Optional

class patient(BaseModel):

    name : str
    age : Annotated[int,Field(gt = 0,title='age',description='Enter your age',examples=[12,34,56])]
    email : EmailStr
    contact_details : Optional[Dict[str,str]] = None

    @field_validator('email')
    @classmethod
    def check_email(cls,value):
        print("abhayyy")
        domain_name = value.split('@')[-1]

        if domain_name not in emails_tag:
            raise ValueError('Not a valid domain')
        return value

    @field_validator('name')
    @classmethod
    def transform_name(cls,value):
        return value.upper()

    @field_validator('age',mode='before')
    @classmethod
    def validate_age(cls,value):
        if 0<value<100:
            return value
        raise ValueError("age should be between 1 and 100")

    @model_validator(mode='after')
    def validate_emergeny_contact(cls,model):
        if model.age > 10 and 'emergency' not in model.contact_details:
            raise ValueError('patient older that 30 must have emergency number')
        return model
            

def insert_data(patient1:patient):
    print(patient1.name)
    print(patient1.age)
    print(patient1.email)

data = {'name' : 'abhay','age':20,'email':'aman@hdfc.com','contact_details' : {'dhd' : '24348738'}}

emails_tag = ['hdfc.com','icici.com']



patient1 = patient(**data)

insert_data(patient1)



