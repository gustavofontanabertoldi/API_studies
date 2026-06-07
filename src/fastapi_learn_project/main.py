from fastapi import FastAPI, HTTPException
from fastapi_learn_project.models.item_model import Item

from contextlib import asynccontextmanager

from .db.database import create_db_and_tables, SessionDep, engine

@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

'''
App começa daqui pra baixo
'''

@app.post("/items/create_item")
async def create_item(new_item:Item, session: SessionDep) -> Item:
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item

@app.get("/items/{item_id}")
async def get_item(id:int, session:SessionDep) -> Item:
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="item nao encontrado")
    return item

@app.delete("/item/delete/{name}")
async def delete_item(id:int, session:SessionDep) -> Item:
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="item nao encontrado")
    session.delete(item)
    session.commit()
    return {"ok":True}