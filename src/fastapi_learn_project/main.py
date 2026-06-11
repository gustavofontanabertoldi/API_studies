from fastapi import FastAPI
from contextlib import asynccontextmanager

from .db.database import create_db_and_tables, engine
from .router.routes import item_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield
    engine.dispose()

app = FastAPI(lifespan=lifespan)

@app.get("/")
async def root():
    return {
        "message": "API rodando perfeitamente!",
        "status": "healthy",
        "docs": "/docs"
    }

app.include_router(item_router)