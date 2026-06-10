from sqlmodel import Field, SQLModel

class ItemBase(SQLModel):
    name:str = Field(index=True)
    price:float | None = Field(default=None, index=True)

class Item (ItemBase, table=True):
    item_id:int | None = Field(default=None, primary_key=True)

class ItemPublic(ItemBase):
    item_id:int
    description:str | None = None

class CreateItem(ItemBase):
    description:str | None = Field(default=None)

class ItemUpdate(ItemBase):
    name:str | None = None
    price:float | None = None
    description:str | None = None