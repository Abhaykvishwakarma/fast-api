from passlib.context import CryptContext   

pwd_context = CryptContext(schemes=["bcrypt"],deprecated="auto")  #-->here we are telling passlib, what is the default hashing alogorithm or what hashing algorithm do we want to use? In this case, we want to use bcrypt 

def hash(password : str):
    return  pwd_context.hash(password)

def verify(plain_password,hashed_password):
    return pwd_context.verify(plain_password,hashed_password)