from contextpilot.context.freshness import check_source
from contextpilot.context.planner import plan
from contextpilot.context.repo_indexer import search_repo
from contextpilot.router.classifier import classify
from contextpilot.storage.repositories import retrieve_memory, store_memory


def plan_request(prompt: str):
    c = classify([{"role": "user", "content": prompt}])
    return {"classification": c.model_dump(), "plan": plan(c)}


def get_context_pack(prompt: str, repo_path: str = "."):
    return {"query": prompt, "results": search_repo(repo_path, prompt)[:10]}


def check_freshness(source: str):
    return check_source(source)


def fetch_and_index_source(path: str):
    return search_repo(path, "")


def retrieve_memory_tool(key: str):
    return retrieve_memory(key)


def store_memory_tool(key: str, value: str):
    store_memory(key, value)
    return {"ok": True}


def explain_route(prompt: str):
    c = classify([{"role": "user", "content": prompt}])
    p = plan(c)
    return {"task_type": c.task_type, "model_tier": c.recommended_model_tier, "strategy": p["strategy"]}
