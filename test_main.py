from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_health():

    response = client.get("/health")

    assert response.status_code == 200

    assert response.json() == {
        "status": "healthy"
    }
def test_get_all_incidents():

    response = client.get("/")

    assert response.status_code == 200

    assert isinstance(response.json(), list)
def test_create_incident():

    response = client.post(
        "/incident",
        json={
            "title": "Test Incident",
            "description": "Testing incident creation",
            "severity": "Low",
            "status": "Open"
        }
    )

    assert response.status_code == 200

    data = response.json()

    assert data["title"] == "Test Incident"
