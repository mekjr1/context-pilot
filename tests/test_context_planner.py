from contextpilot.router.classifier import classify
from contextpilot.context.planner import plan
def test_plan_docs(): assert plan(classify([{"role":"user","content":"latest API docs"}]))["strategy"]=="docs_freshness"
