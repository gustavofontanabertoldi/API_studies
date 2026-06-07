from sqlmodel import Field, SQLModel

class Item(SQLModel, table=True):
    item_id:int | None = Field(default=None, primary_key=True)
    name:str = Field(index=True)
    price:float | None = Field(default=None, index=True)
    description:str | None = Field(default=None)