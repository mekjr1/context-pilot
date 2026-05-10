from fastapi import FastAPI
from contextpilot.api.health import router as h
from contextpilot.api.models import router as m
from contextpilot.api.openai import router as o
from contextpilot.api.anthropic import router as a
from contextpilot.storage.migrations import init_db

app = FastAPI()
app.include_router(h)
app.include_router(m)
app.include_router(o)
app.include_router(a)


@app.on_event("startup")
def startup():
    init_db()
