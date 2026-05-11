"""
Testes de integração da API (camada HTTP).

Usa o TestClient do FastAPI: sobe a aplicação em memória e faz requisições
reais contra os endpoints, sem precisar de servidor rodando. Combinado
com os testes unitários da calculadora, dá uma cobertura completa.
"""

from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_root_retorna_mensagem_de_boas_vindas():
    response = client.get("/")
    assert response.status_code == 200
    body = response.json()
    assert body["service"] == "calculadora-api"
    assert "message" in body


def test_health_check():
    # Esse endpoint é usado pelo pipeline depois do deploy, no smoke test
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_add_endpoint():
    response = client.get("/add", params={"a": 7, "b": 3})
    assert response.status_code == 200
    assert response.json()["result"] == 10


def test_subtract_endpoint():
    response = client.get("/subtract", params={"a": 10, "b": 4})
    assert response.status_code == 200
    assert response.json()["result"] == 6


def test_multiply_endpoint():
    response = client.get("/multiply", params={"a": 6, "b": 7})
    assert response.status_code == 200
    assert response.json()["result"] == 42


def test_divide_endpoint_caso_normal():
    response = client.get("/divide", params={"a": 20, "b": 4})
    assert response.status_code == 200
    assert response.json()["result"] == 5


def test_divide_por_zero_retorna_400():
    # O comportamento esperado é converter o ValueError em uma resposta
    # HTTP 400 (Bad Request) bem informativa para o cliente da API.
    response = client.get("/divide", params={"a": 10, "b": 0})
    assert response.status_code == 400
    assert "Divisão por zero" in response.json()["detail"]


def test_parametros_invalidos_retornam_422():
    # FastAPI valida automaticamente os tipos. Texto onde se espera
    # número deve devolver 422 (Unprocessable Entity).
    response = client.get("/add", params={"a": "abc", "b": 3})
    assert response.status_code == 422
