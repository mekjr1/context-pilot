import json

from contextpilot.storage.db import SessionLocal
from contextpilot.storage.models import FreshnessCheck, Memory, RouteDecision, Trace


def write_trace(route: str, payload: str) -> None:
    with SessionLocal() as session:
        session.add(Trace(route=route, payload=payload))
        session.commit()


def write_route(task_type: str, model_tier: str) -> None:
    with SessionLocal() as session:
        session.add(RouteDecision(task_type=task_type, model_tier=model_tier))
        session.commit()


def list_traces(limit: int = 20):
    with SessionLocal() as session:
        return session.query(Trace).order_by(Trace.id.desc()).limit(limit).all()


def store_memory(key: str, value: str) -> None:
    with SessionLocal() as session:
        session.add(Memory(key=key, value=value))
        session.commit()


def retrieve_memory(key: str, limit: int = 5) -> list[dict]:
    with SessionLocal() as session:
        rows = (
            session.query(Memory)
            .filter(Memory.key == key)
            .order_by(Memory.id.desc())
            .limit(limit)
            .all()
        )
    return [{"id": r.id, "key": r.key, "value": r.value} for r in rows]


def write_freshness_check(source: str, check_type: str, metadata: dict) -> None:
    with SessionLocal() as session:
        session.add(
            FreshnessCheck(source=source, check_type=check_type, metadata=json.dumps(metadata))
        )
        session.commit()
