from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

# arranque: uvicorn users:app --reload
router = APIRouter()

# Entidad user

class User(BaseModel):
    id: int
    name: str
    surname: str
    url: str
    age: int


users_list = [
    User(id = 1, name="Brais", surname="Moure", url="https://moure.dev", age=35),
    User(id = 2, name="Moure", surname="Dev", url="https://mouredev.com", age=35),
    User(id = 3, name="Haakon", surname="Dahlberg", url="https://hakoon.com", age=33)
]


def search_user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}


@router.get("/users_json")
async def users_json():
    return [{"name": "Brais", "surname": "Moure", "url": "https://moure.dev", "age": 35},
            {"name": "Moure", "surname": "Dev", "url": "https://mouredev.com", "age": 35},
            {"name": "Haakon", "surname": "Dahlberg", "url": "https://hakoon.com", "age": 33}]

##################
### get
##################
@router.get("/users")
async def users():
    return users_list

# parametros por path
# @app.get("/user/{id}")
# async def user(id: int):
#     return search_user(id)
    
# # parametros por query
# @app.get("/userquery/")
# async def userquery(id: int):
#     return search_user(id)

# podemos hacer que sean lo mismo
# parametros por path
@router.get("/user/{ide}")
async def user(ide: int):
    return search_user(ide)
    
# parametros por query
@router.get("/user/")
async def userquery(id: int):
    return search_user(id)

##################
### post
##################


@router.post("/user/", response_model = User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    users_list.append(user)
    return user

##################
### put
##################

@router.put("/user/")
async def user(user: User):

    found = False

    for index, saved_user in enumerate(users_list):
        if saved_user.id == user.id:
            users_list[index] = user
            found = True

    if found:
        return user
        
    else:
        return {"error": "no se ha actualizado el usuario"} 


##################
### delete
##################

# lo podemos hacer por path o por query. aqui lo suyo seria por path

@router.delete("/user/{id}")
async def user(id: int):

    found = False
    for index, saved_user in enumerate(users_list):
        if saved_user.id == id:
            del users_list[index]
            found = True
    
    if found:
        return {"info": f"usuario con id {id} eliminado"}
    else:
        return {"error": "no se ha encontrado el usuario"}