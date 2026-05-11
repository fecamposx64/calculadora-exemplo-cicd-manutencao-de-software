# Calculadora API

API simples em FastAPI usada como projeto-exemplo para CI/CD com GitHub Actions.

## Objetivo

Mostrar um fluxo completo de lint, testes, build e deploy simulados em um projeto pequeno
com separacao entre logica de negocio e camada HTTP.

## Endpoints

- `GET /` mensagem de boas-vindas
- `GET /health` healthcheck
- `GET /add?a=1&b=2`
- `GET /subtract?a=10&b=3`
- `GET /multiply?a=4&b=5`
- `GET /divide?a=10&b=2`

## Requisitos

- Python 3.11 ou 3.12

## Setup local

```bash
python3 -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## Rodar a API

```bash
uvicorn app.main:app --reload
# http://localhost:8000/docs
```

## Testes e lint

```bash
ruff check app tests
ruff format --check app tests
pytest
```

## CI/CD

O workflow em .github/workflows/ci-cd.yml executa lint, testes em matrix (3.11 e 3.12),
smoke test do build e um deploy simulado quando ha push na main.
