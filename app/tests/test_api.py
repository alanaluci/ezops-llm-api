import pytest
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

@pytest.mark.parametrize("input_text, expected_response", [
    ("2 + 2", "Resultado da expressão matemática: 4"),
    ("O que é inteligência artificial?", "Wikipedia Search"),
    ("Olá, como você está?", None)  # Nenhuma ferramenta deve ser usada
])
def test_infer(input_text, expected_response):
    response = client.post("/infer", json={"text": input_text})
    assert response.status_code == 200
    data = response.json()

    if expected_response:
        assert expected_response in data["response"] or expected_response in data["tools_used"]
    else:
        assert not data["tools_used"]
