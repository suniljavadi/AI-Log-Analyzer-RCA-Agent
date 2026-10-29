import pytest
from fastapi.testclient import TestClient

from app.api.main import app
from app.config import Settings


def test_ready_checks_database():
    with TestClient(app) as client:
        response = client.get("/ready")
    assert response.status_code == 200
    assert response.json()["database"] == "ok"


def test_request_id_is_propagated():
    with TestClient(app) as client:
        response = client.get("/health", headers={"X-Request-ID": "abc-123"})
    assert response.headers["X-Request-ID"] == "abc-123"


def test_unhandled_error_returns_500_with_request_id():
    def boom():
        raise RuntimeError("boom")

    app.add_api_route("/_boom", boom)
    try:
        with TestClient(app, raise_server_exceptions=False) as client:
            response = client.get("/_boom")
    finally:
        app.router.routes.pop()
    assert response.status_code == 500
    assert response.json()["detail"] == "Internal server error"
    assert "X-Request-ID" in response.headers


def test_openai_mode_requires_api_key():
    with pytest.raises(ValueError):
        Settings(_env_file=None, llm_mode="openai", openai_api_key=None)


def test_invalid_llm_mode_rejected():
    with pytest.raises(ValueError):
        Settings(_env_file=None, llm_mode="bogus")