import os
from unittest import mock
from fastapi.testclient import TestClient
from app.main import app , DEFAULT_CONFIG
import pytest

client = TestClient(app)

def test_health():
    """
    Verifica que el endpoint /health responda 200 OK.
    Requisito para Liveness/Readiness Probes.
    """
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}

def test_config_defaults():
    """
    Verifica que el endpoint /config devuelva los valores por defecto si no encuentra valores
    """
    with mock.patch.dict(os.environ, {}, clear=True):
        response = client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert data["config"]["app_mode"] == DEFAULT_CONFIG["APP_MODE"]
        assert data["config"]["log_level"] == DEFAULT_CONFIG["LOG_LEVEL"]
        assert data["config"]["max_retries"] == DEFAULT_CONFIG["MAX_RETRIES"]
        assert data["config"]["target_system"] == DEFAULT_CONFIG["TARGET_SYSTEM"]
        assert "..." in data["secrets"]["api_key_masked"]


VALID_VARIABLES=[
    {
        "APP_MODE": "Dev",
        "LOG_LEVEL": "DEBUG",
        "MAX_RETRIES":"3",
        "TARGET_SYSTEM":"test-db",
        "API_KEY": "secret-api-key-123456",
    },
    {
        "APP_MODE": "Dev",
        "LOG_LEVEL": "Warning",
        "MAX_RETRIES":"10",
        "TARGET_SYSTEM":"test-db-2",
        "API_KEY": "secret-api-key-938348",
    }
    ]

@pytest.mark.parametrize("VARIABLES",VALID_VARIABLES)
def test_config_custom(VARIABLES):
    """
    Verifica que endpoint /config devuelva valores correctos
    """

    with mock.patch.dict(os.environ, VARIABLES, clear=True):
        response = client.get("/config")
        assert response.status_code == 200
        data = response.json()
        assert data["config"]["app_mode"] == VARIABLES["APP_MODE"]
        assert data["config"]["log_level"] == VARIABLES["LOG_LEVEL"].upper()
        assert data["config"]["max_retries"] == int(VARIABLES["MAX_RETRIES"])
        assert data["config"]["target_system"] == VARIABLES["TARGET_SYSTEM"]
        assert "..." in data["secrets"]["api_key_masked"]
