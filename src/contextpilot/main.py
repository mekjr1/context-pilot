from contextlib import asynccontextmanager

from fastapi import FastAPI
from contextpilot.api.health import router as h
from contextpilot.api.models import router as m
from contextpilot.api.openai import router as o
from contextpilot.api.anthropic import router as a
from contextpilot.storage.migrations import init_db


@asynccontextmanager
async def lifespan(_: FastAPI):
    init_db()
    yield


app = FastAPI(lifespan=lifespan)
app.include_router(h)
app.include_router(m)
app.include_router(o)
app.include_router(a)
