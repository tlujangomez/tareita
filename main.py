import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from database import db
from vistas import router as vistas_router

DATABASE_URL = "postgresql://neondb_owner:npg_XaP5SpUfD9rj@ep-gentle-poetry-ax2jews9-pooler.c-4.us-east-2.aws.neon.tech/neondb?sslmode=require&channel_binding=require"


@asynccontextmanager
async def lifespan(app: FastAPI):
    await db.connect(DATABASE_URL)
    yield
    await db.close()


app = FastAPI(lifespan=lifespan)

app.include_router(vistas_router)