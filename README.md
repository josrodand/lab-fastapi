# lab-fastapi

Lab repo para trastear con fastapi. 

Fuentes:
* [Curso de youtube de mouredev](https://www.youtube.com/watch?v=_y9qQZXE24A&list=PLNdFk2_brsRdgQXLIlKBXQDeRf3qvXVU_&index=3)
* [repositorio](https://github.com/mouredev/Hello-Python)
* [FastAPI](https://fastapi.tiangolo.com/)


## Notas del video

### ¿Que es una petición asincrona?
Creamos una función asincrona porque no sabemos cuanto va a tardar el servidor en responder.
Con una función asíncrona evitamos que la aplicación se quede bloqueada esperando al servidor.
Cuando creamos una función en fastapi, la creamos asincrona para evitar esto.
```
async def root():
    return {"message": "Hello World"}
```

### Levantar un servidor
una vez tengamos un main.py con el codigo de una api basica, podemos levantar el servidor desde la consola. Para el siguiente código:

```python
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
```
Usamos el siguiente comando:

```powershell
uvicorn main:app --reload
```

>**nota**: main hace referencia a main.py y app a la variable app. si fuesen otros nombres hay que modificarlo.

>**nota**: --reload lo que hace es que lo mantiene levantado de forma de que si modificamos algo en el fichero y lo guardemos, se cambie automáticamente en el servidor.

### documentacion interactiva de fastAPI

Basada en swagger.ui

* Si ponemos la url + /docs nos abre una documentacion interactiva en el propio servidor (swagger)
* Si ponemos la url + /redoc nos abre una documentacion interactiva en el propio servidor (redoc)


### Uso de basemodel

en el ejemplo de users.py estamos viendo como va a crear una clase para definir un usuario. Está usando el objeto BaseModel de pydantic, que permite crear una entidad. Una entidad es como una clase pero orientada a datos. La clase User hereda comportamiento de BaseModel.

Esto nos permite que al devolver con una api esa clase, nos la devuelve como un json:
```python
class User(BaseModel):
    name: str
    surname: str
    url: str
    age: int


@app.get("/userclass")
async def userclass():
    return User(name="Brais", surname="Moure", url="https://moure.dev", age=35)
```

Trabajar con BaseModel nos permite que al devolver objetos o listas de objetos se haga como si fueran json.
```python
users_list = [
    User(name="Brais", surname="Moure", url="https://moure.dev", age=35),
    User(name="Moure", surname="Dev", url="https://mouredev.com", age=35),
    User(name="Haakon", surname="Dahlberg", url="https://hakoon.com", age=33)
]
```


### Path
Usamos el Path para pasar info a la api.

Por ejemplo, el id de un usuario

### Parametros de path y query

Mandar un parametro de path es como ya hemos visto.
```python
@app.get("/user/{id}")
async def user(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
```

Esto respondería si vamos a postman y hacemos get a lo siguiente
```
http://127.0.0.1:8000/user/1
```


Mandar parametros por query es igualar un conjunto clave-valor dentro de la url.
Un parametro por path puede ser un parametro obligatorio, mientras que uno de query es un parámetro opcional.

El servicio anterior con parametros de query sería:

```python
@app.get("/userquery/")
async def userquery(id: int):
    users = filter(lambda user: user.id == id, users_list)
    try:
        return list(users)[0]
    except:
        return {"error": "No se ha encontrado el usuario"}
```

Lo llamariamos asi. Para pasar un parametro los separamos con `?`
```
http://127.0.0.1:8000/userquery/?id=1
```


Podemos hacer que la misma ruta sirva para paso de parametros por path o por query:
```python
# podemos hacer que sean lo mismo
# parametros por path
@app.get("/user/{ide}")
async def user(ide: int):
    return search_user(ide)
    
# parametros por query
@app.get("/user/")
async def userquery(id: int):
    return search_user(id)
```

entonces, obtendriamos lo mismo de las dos formas:
```
http://127.0.0.1:8000/user/1
http://127.0.0.1:8000/user/?id=1
```

si ponemos mas parametros, se ponen separados con un aspersan
```
http://127.0.0.1:8000/user/?id=1&name=brais
```

convenio para usar path o query con los parametros:
* path se usa cuando consideramos que es un parámetro obligatorio o fijo
* query para parámetros que pueden no ser necesarios

Realmente lo que hemos hecho de pasar la id por query no deberiamos hacerlo

# Operacin POST

Hacemos un post simple par ainsertar un usuario nuevo en la base de datos, que ahora mismo es una lista.

```python
@app.post("/user/")
async def user(user: User):
    if type(search_user(user.id)) == User:
        return {"error": "El usuario ya existe"}
    else:
        users_list.append(user)
        return user
```
Simplemente indicamos que toma como entrada un objeto de clase User, y se inserta en la lista. Indicamos que devuelva un error si ya está en la lista.


# Operacion PUT

Usamos PUT para modificar la info de un usuario. Le mandamos como entrada un JSON con los datos de un usuario, y el servicio lo buscará por id y actualizará. Si el id no se encuentra se devuelve un mensaje de error.

```python
@app.put("/user/")
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
```



# Operacion DELETE

Usamos DELETE para eliminar registros en nuestra lista de usuarios.

Ejemplo de servicio:

```python
@app.delete("/user/{id}")
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
```

en este caso le pasamos solo el id. Lo hacemos por path aunque ambién podría hacerse por query. Sin embargo se supone que es mas recomendable hacerlo por path.



# HTTP status code

ahora mismo tenemos mensajes de error cuando no funciona, pero devuelve el 200 ok, y eso es que la cosa ha ido bien segun el protocolo http.

* [Listado de códigos http](https://developer.mozilla.org/en-US/docs/Web/HTTP/Status)

Hay unos códigos que son mas frecuentes que otros. En la [documentación de fastAPI](https://fastapi.tiangolo.com/tutorial/response-status-code/) vienen recogidos.

Para devolver un codigo especifico lo incluimos en la parte de definición de ruta `@app.___`

Modificamos la ruta de post para incluir el mensaje 201, que indica que se ha creado un recurso.

```python
@app.post("/user/", status_code=201)
```

También modificamos que devuelva un codigo concreto cuando se produzca el error. Por ejemplo 404 not found, o un 409 conflict. Tambien sirve 304 not modified. Vamos a usar 404.

Para esto tenemos que devolver una excepcion, una clase de exception que esta en fastapi.

También añadimos en la ruta el parámetro response_model. Lo teníamos montado para que devuelva un objeto User, así que se lo indicamos.

```python
@app.post("/user/", response_model = User, status_code=201)
async def user(user: User):
    if type(search_user(user.id)) == User:
        raise HTTPException(status_code=404, detail="El usuario ya existe")
    
    users_list.append(user)
    return user
```

Se deja como ejercicio cambiar los status code de todas las rutas de users.py.


# Routers

Ahora mismo la API funciona, pero hay que darle un enfoque para que tenga mas sentido.

Vamos a crear `productos.py` con otra api para llamar productos.

```python

from fastapi import FastAPI

app = FastAPI()

@app.get("/products")
async def products():
    return ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]
```

Lo suyo es tener los servicios agrupados según los criterios necesarios. en este caso tendríamos la API de usuarios por un lado y la de productos por otro. Podríamos levantar la de productos pero no tendríamos acceso a la de usuarios.

Lo que pasa es que si tenemos levantada la de users, no podemos lanzarle peticiones a la de products.

¿Tendríamos entonces que levantar varios proyectos?

Aqui es donde entra el concepto de **enrutamiento**.

Creamos un directorio llamado routers. Metemos users y products dentro.

Lo que queremos es tener una API general que actue de router, para que llame a las dos que tenemos.

Para ello hacemos lo siguiente: En vez de FastAPI importamos APIRouter, y en vez de crear un elemento app creamos router.

En productos.py quedaria asi:

```python
from fastapi import APIRouter

router = APIRouter()

@router.get("/products")
async def products():
    return ["Producto 1", "Producto 2", "Producto 3", "Producto 4", "Producto 5"]
```

ahora desde ``main.py`` importamos products. Quedaría asi:

```python
from fastapi import FastAPI

from routers import products

app = FastAPI()

# routers
app.include_router(products.router)


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.get("/url")
async def url():
    return {"url_curso": "https://mouredev.com/python"}

```

Lo que hacemos es importar el script productos del directorio routers. Luego se lo indicamos con `app.include_router(products.router)`.

ahora, si arrancamos main podriamos lanzar peticiones a las rutas de productos.

Hacemos lo mismo con `users.py`

> **Nota**: al cambiar la variable app por router hay que cambiar todos los @. (``@app.get(...)`` ahora es ``@router.get(...)``)

Hecho esto solo tendríamos que añadirlo a nuestro `main.py`

```python
from fastapi import FastAPI
from routers import products, users

app = FastAPI()

# routers
app.include_router(products.router)
app.include_router(users.router)
```
si ahora levantamos main con `uvicorn main:app --reload`, todo lo hecho hasta ahora debe funcionar.

Lo suyo es que en cada script de rutas del directorio routers, cada uno tenga siempre referenciado la misma ruta (que tengan el mismo path). Esto es que todas las de users la ruta sea `/users/...` y en products todas sean `/products/`.

tenemos alguna rara en users como `/usersjson/` que podriamos mover a otro fichero.

Modificamos Products añadiendo una ruta mas de acceso por un id. Además, añadimos un prefijo en `APIRouter()` para que siempre sea el path `/products`. También añadimos el parámetro response para que devuelva un error 404 si no encuentra por id.

> **Nota**: el parametro tags hace que las rutas de la api se agrupen luego en la documentacion.

```python
from fastapi import APIRouter

router = APIRouter(
    prefix="/products",
    tags=["products"],
    responses={404: {"message": "not found"}}
)


products_list = [
    "Producto 1", 
    "Producto 2", 
    "Producto 3", 
    "Producto 4", 
    "Producto 5"
    ]


@router.get("/")
async def products():
    return products_list


@router.get("/{id}")
async def products(id: int):
    return products_list[id]
```

Se deja como tarea ajustar el fichero de users con los cambios que hemos hecho en products. Por ejemplo, separar users_json en otro router.











