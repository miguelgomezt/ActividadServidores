# Para instalar dependencias
# pip install fastapi uvicorn

# Para iniciar el servicio
# uvicorn main:app --reload

from fastapi import FastAPI
from pydantic import BaseModel
import sqlite3
from datetime import datetime   

conexion = sqlite3.connect("items.db", check_same_thread=False)
cursor = conexion.cursor()
cursor.execute("""
    CREATE TABLE IF NOT EXISTS items (
        id         INTEGER PRIMARY KEY AUTOINCREMENT,
        name       TEXT,
        price      REAL,
        created_at TEXT
    )
""")
conexion.commit()


class Item(BaseModel): # BaseModel es una clase que nos va permitir validar el envío de datos por POST
    name: str = 'Mateo'
    price: float = 2000.35


class ItemResponse(BaseModel): 
    id: int 
    name: str
    price: float
    created_at: str



app = FastAPI()


# endpoint: el punto al cual yo quiero llamar de nuestra API
@app.get("/")
def read_root():
    return {"message": "Universidad EIA"}

@app.get("/items/")
def read_items(): 
    cursor.execute("Select id, name, price, created_at FROM items")
    filas = cursor.fetchall()
    return[{"id": f[0], "name": f[1], "price": f[2], "created_at": f[3]} for f in filas]

@app.post("/items/")
def create_item(item: Item):
    ahora = datetime.utcnow().isoformat()
    cursor.execute(
        "INSERT INTO items (name, price, created_at) VALUES (?, ?, ?)",
        (item.name, item.price, ahora)
    )
    conexion.commit()
    return {"id": cursor.lastrowid, "name": item.name, "price": item.price, "created_at": ahora}
   

