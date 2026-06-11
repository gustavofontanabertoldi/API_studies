from fastapi import HTTPException, APIRouter, Depends
from typing import Annotated

from fastapi_learn_project.models.item_model import Item, ItemPublic, CreateItem, ItemUpdate
from fastapi_learn_project.db.database import SessionDep
from fastapi_learn_project.core.auth import oauth2_scheme

item_router = APIRouter()

@item_router.post("/items/create_item", response_model=ItemPublic)
async def create_item(item_in:CreateItem, session: SessionDep):
    new_item = Item.model_validate(item_in)
    session.add(new_item)
    session.commit()
    session.refresh(new_item)
    return new_item

@item_router.get("/items/{item_id}", response_model=ItemPublic)
async def get_item(id:int, session:SessionDep, token:Annotated[str, Depends(oauth2_scheme)]):
    item = session.get(Item, id)
    if not item:
        raise HTTPException(status_code=404, detail="item nao encontrado")
    return item

@item_router.delete("/item/delete/{item_id}")
async def delete_item(item_id:int, session:SessionDep):
    item = session.get(Item, item_id)
    if not item:
        raise HTTPException(status_code=404, detail="item nao encontrado")
    session.delete(item)
    session.commit()
    return {"ok":True}

@item_router.patch("/items/update/{item_id}", response_model=ItemPublic)
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