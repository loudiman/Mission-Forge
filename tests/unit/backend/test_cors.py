import pytest
from fastapi.testclient import TestClient
from src.missionforge.backend.main import app

client = TestClient(app)

def test_cors_headers():
    response = client.options(
        "/api/missions",
        headers={
            "Origin": "http://localhost:3000",
            "Access-Control-Request-Method": "GET"
        }
    )
    assert response.status_code == 200
    assert response.headers.get("access-control-allow-origin") == "http://localhost:3000"
    assert "access-control-allow-methods" in response.headers
