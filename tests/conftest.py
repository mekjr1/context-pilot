import pytest


@pytest.fixture
def auth_headers():
    return {"Authorization": "Bearer local-dev-key"}
