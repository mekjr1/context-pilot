import json

import typer
import uvicorn

from contextpilot.context.freshness import check_source
from contextpilot.context.planner import plan
from contextpilot.context.repo_indexer import index_repo, search_repo
from contextpilot.main import app as fastapi_app
from contextpilot.router.classifier import classify
from contextpilot.storage.repositories import list_traces

app = typer.Typer()


@app.command()
def serve(host: str = "127.0.0.1", port: int = 8787):
    uvicorn.run(fastapi_app, host=host, port=port)


@app.command("classify")
def classify_cli(text: str):
    print(classify([{"role": "user", "content": text}]).model_dump_json(indent=2))


@app.command("plan")
def plan_cli(text: str):
    c = classify([{"role": "user", "content": text}])
    print(json.dumps(plan(c), indent=2))


@app.command("add-repo")
def add_repo(path: str):
    print(json.dumps({"added": path}))


@app.command("index-repo")
def index_repo_cli(path: str):
    print(len(index_repo(path)))


@app.command("search-repo")
def search_repo_cli(q: str, path: str = "."):
    print(json.dumps(search_repo(path, q), indent=2))


@app.command("check-source")
def check_source_cli(source: str):
    print(json.dumps(check_source(source), indent=2))


@app.command()
def models():
    print("contextpilot-auto")


@app.command()
def traces(limit: int = 20):
    rows = list_traces(limit=limit)
    print(json.dumps([{"id": r.id, "route": r.route} for r in rows], indent=2))
