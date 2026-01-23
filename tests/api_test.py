from fastapi.testclient import TestClient
from api.main import app

client = TestClient(app)

def test_api_ask(mocker):
    mocker.patch(
        "api.main.answer",
        return_value="Réponse mockée"
    )

    response = client.post(
        "/ask",
        json={"question": "Que faire ce week-end ?"}
    )

    assert response.status_code == 200
    assert "Réponse mockée" in response.json()["answer"]
