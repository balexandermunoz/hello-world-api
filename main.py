#Python
from typing import Optional
from enum import Enum

#Pydantic
from pydantic import BaseModel
from pydantic import Field, EmailStr

#FastAPI
from fastapi import FastAPI
from fastapi import Body, Query, Path

app = FastAPI()

# Models

class HairColor(Enum):
    white = "white"
    brown = "brown"
    blonde = "blonde"
    red = "red"
    

class Location(BaseModel):
    city: str = Field(min_length=1, max_length=50)
    state: str = Field(min_length=1, max_length=50)
    country: str = Field(min_length=1, max_length=50)

class Person(BaseModel):
    first_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Miguel"
        )
    last_name: str = Field(
        ...,
        min_length=1,
        max_length=50,
        example="Torres"
        )
    age: int = Field(
        ...,
        gt=0,
        lt=115,
        example=25
    )
    email: EmailStr = Field(
        ...,   
    )
    hair_color: Optional[HairColor] = Field(default=None)
    is_married: Optional[bool] = Field(default=None)
    
    # Para tener un ejemplo predeterminado: 
    # class Config:
    #     schema_extra = {
    #         "example": {
    #             "first_name": "Facundo",
    #             "last_name": "García Martoni",
    #             "age": 21,
    #             "hair_color": "blonde",
    #             "is_married": False
    #         }
    #     }


@app.get("/")
def home():
    return {"hello": "world"}


# Rqeuest and Response Body

#(...) Obligatorio!
@app.post("/person/new")
def create_person(person: Person = Body(...)):
    return person

# Validaciones: Query parameters

@app.get("/person/detail")
def show_person(
    name: Optional[str] = Query(
        None,
        min_length=1,
        max_length=50,
        title="Person name",
        description="This is the person name. It's between 1 and 50 characters"
        ),
    age: Optional[int] = Query(
        ...,  # Lo ideal es que el query parameter sea opcional no (...)
        title="Person age",
        description="This is the person age"
        )
):
    return {name: age}


# Validaciones: Path parameters

@app.get("/person/detail/{person_id}")
def show_person(
    person_id: int = Path(
        ..., # Obligatorio
        gt=0, # Greather than 0
        title="Person id",
        description="This is the person id"
    )
):
    return {person_id: "Exist!"}

# Validaciones: Request Body

@app.put("/person/{person_id}")
def update_person(
    person_id: int = Path(
        ...,
        title="Person ID",
        description="This is the person ID"
        ),
    person: Person = Body(...),
    location: Location = Body(...),
    ):
    # Two request bodies: 
    results = person.dict()
    results.update(location.dict())
    
    return results