from fastapi import FastAPI
from fastapi.testclient import TestClient

from src.missionforge.backend.routers.missions import get_repository, router

app = FastAPI()
app.include_router(router)

client = TestClient(app)

class MockRepository:
    def __init__(self):
        pass

    def list_missions(self):
        return ["MF-001"]

    def read_mission_yaml(self, mission_id):
        if mission_id == "MF-001":
            return {
                "id": "MF-001",
                "goal": "Test goal",
                "sub_missions": ["MF-001-A"]
            }
        return None

    def read_sub_mission_yaml(self, mission_id, sub_id):
        if sub_id == "MF-001-A":
            return {
                "id": "MF-001-A",
                "parent": "MF-001",
                "title": "Sub A",
                "status": "PASSED"
            }
        return None

    def read_report(self, mission_id):
        if mission_id == "MF-001":
            return "# Report"
        return None

app.dependency_overrides[get_repository] = lambda: MockRepository()

def test_list_missions():
    response = client.get("/api/missions")
    assert response.status_code == 200
    assert len(response.json()) == 1
    assert response.json()[0]["id"] == "MF-001"

def test_get_mission():
    response = client.get("/api/missions/MF-001")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "MF-001"
    assert data["goal"] == "Test goal"
    assert len(data["sub_missions"]) == 1

def test_list_sub_missions():
    response = client.get("/api/missions/MF-001/sub-missions")
    assert response.status_code == 200
    data = response.json()
    assert len(data) == 1
    assert data[0]["id"] == "MF-001-A"
    assert data[0]["title"] == "Sub A"

def test_get_sub_mission():
    response = client.get("/api/missions/MF-001/sub-missions/MF-001-A")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == "MF-001-A"
    assert data["title"] == "Sub A"

def test_get_report():
    response = client.get("/api/missions/MF-001/report")
    assert response.status_code == 200
    assert response.json()["content"] == "# Report"

