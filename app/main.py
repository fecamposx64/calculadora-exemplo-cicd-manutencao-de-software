"""
API FastAPI da calculadora.

Endpoints expostos:
  GET /            -> mensagem de boas-vindas
  GET /health      -> healthcheck (usado pelo job de smoke test do pipeline)
  GET /add         -> soma  (?a=1&b=2)
  GET /subtract    -> sub.  (?a=10&b=3)
  GET /multiply    -> mult. (?a=4&b=5)
  GET /divide      -> div.  (?a=10&b=2)
"""

from fastapi import FastAPI, HTTPException

from app import calculator

app = FastAPI(
    title="Calculadora API",
    description="Projeto-demo para a aula de CI/CD",
    version="1.0.0",
)


@app.get("/")
def root() -> dict:
    return {
        "service": "calculadora-api",
        "message": "Olá! Esta API é o exemplo do pipeline CI/CD.",
        "version": app.version,
    }


@app.get("/health")
def health() -> dict:
    return {"status": "ok"}


@app.get("/add")
def add_endpoint(a: float, b: float) -> dict:
    return {"operation": "add", "a": a, "b": b, "result": calculator.add(a, b)}


@app.get("/subtract")
def subtract_endpoint(a: float, b: float) -> dict:
    return {"operation": "subtract", "a": a, "b": b, "result": calculator.subtract(a, b)}


@app.get("/multiply")
def multiply_endpoint(a: float, b: float) -> dict:
    return {"operation": "multiply", "a": a, "b": b, "result": calculator.multiply(a, b)}


@app.get("/divide")
def divide_endpoint(a: float, b: float) -> dict:
    try:
        return {"operation": "divide", "a": a, "b": b, "result": calculator.divide(a, b)}
    except ValueError as exc:
        # Convertemos a regra de negócio em uma resposta HTTP adequada
        raise HTTPException(status_code=400, detail=str(exc)) from exc
