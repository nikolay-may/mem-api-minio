from contextlib import asynccontextmanager
import logging

from fastapi import FastAPI
from public_api.routes import memes
from db_service.db_init import create_all_tables, delete_all_tables

logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app: FastAPI):
    await create_all_tables()
    yield
    await delete_all_tables()


app = FastAPI(lifespan=lifespan)

app.include_router(memes.router)


@app.get("/")
def read_root():
    return {"message": "Welcome !"}
