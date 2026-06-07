from sqlmodel import create_engine, SQLModel, Session
from fastapi import Depends

from typing import Annotated
from pathlib import Path

ROOT_DIR = Path(__file__).resolve().parent.parent.parent.parent
sqlite_file_path = ROOT_DIR / "database.db"
sqlite_url = f"sqlite:///{sqlite_file_path}"

connect_args = {"check_same_thread":False}
engine = create_engine(sqlite_url, connect_args=connect_args)

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session

SessionDep = Annotated[Session, Depends(get_session)]