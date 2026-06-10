from fastapi import FastAPI, HTTPException
from fastapi_learn_project.models.item_model import Item, ItemPublic, CreateItem, ItemUpdate

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

@app.post("/items/create_item", response_model=ItemPublic)
async def create_item(item_in:CreateItem, session: SessionDep):
    new_item = Item.model_validate(item_in)
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item

@app.get("/items/{item_id}", response_model=ItemPublic)
async def get_item(id:int, session:SessionDep):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="item nao encontrado")
    return item

@app.delete("/item/delete/{item_id}")
async def delete_item(item_id:int, session:SessionDep):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item nao encontrado")
    session.delete(item)
    session.commit()
    return {"ok":True}

@app.patch("/items/update/{item_id}", response_model=ItemPublic)
async def update_item(item_id:int, item_in:ItemUpdate, session:SessionDep):
    item_db = session.get(Item, item_id)
    if not item_db:
        raise HTTPException(status_code=404, detail="item nao encontrado")
    item_data = item_in.model_dump(exclude_unset=True)
    item_db.sqlmodel_update(item_data)
    session.add(item_db)
    session.commit()
    session.refresh(item_db)
    return item_db