from fastapi.testclient import TestClient
from contextpilot.main import app
def test_models(): assert TestClient(app).get("/v1/models").status_code==200
def test_chat():
 r=TestClient(app).post("/v1/chat/completions",json={"model":"contextpilot-auto","messages":[{"role":"user","content":"hi"}]}); assert r.status_code==200
def test_stream():
 r=TestClient(app).post("/v1/chat/completions",json={"model":"contextpilot-auto","messages":[{"role":"user","content":"hi"}],"stream":True}); assert r.status_code==200
