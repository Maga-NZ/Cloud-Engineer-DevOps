from unittest.mock import MagicMock, patch

import pytest

import app as flask_app


@pytest.fixture
def client():
    flask_app.app.config["TESTING"] = True
    with flask_app.app.test_client() as client:
        yield client


def test_index_returns_running_status(client):
    response = client.get("/")
    assert response.status_code == 200
    payload = response.get_json()
    assert payload["status"] == "running"
    assert "version" in payload


def test_metrics_endpoint_is_exposed(client):
    response = client.get("/metrics")
    assert response.status_code == 200
    assert b"http_requests_total" in response.data


@patch("app.get_db_connection")
def test_health_reports_healthy_when_db_reachable(mock_conn, client):
    mock_conn.return_value = MagicMock()
    response = client.get("/health")
    assert response.status_code == 200
    assert response.get_json()["status"] == "healthy"


@patch("app.get_db_connection", side_effect=Exception("connection refused"))
def test_health_reports_unhealthy_when_db_down(_mock_conn, client):
    response = client.get("/health")
    assert response.status_code == 500
    assert response.get_json()["status"] == "unhealthy"
