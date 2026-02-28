from pydantic import BaseModel, EmailStr
# from typing import Optional

class TokenSchema(BaseModel):

    sub : str
    role: str

class CreateUser(BaseModel):

    full_name : str
    email : EmailStr | None = None
    password : str 
    role : str | None = None

class CreateSchool(BaseModel):

    name: str
    adress : str

class SchoolOut(BaseModel):

    id: int
    name: str
    adress: str

class UserOut(BaseModel):

    id: int
    full_name: str
    email: EmailStr | None = None
    role: str
    school_id: int | None = None

    class Config:
        orm_mode = True


class CreateTurma(BaseModel):
    
    name: str
    number_of_students: int | None = 0
    class_director_id: int | None = None
    class_section: str | None = None

class CreateStudent(BaseModel):
    
    full_name: str
    email: EmailStr | None = None
    turma_name: str | None = None
    age: int | None = None
    fathers_name: str | None = None
    mothers_name: str | None = None
    adress: str | None = None