import pytest
from backend.settings import settings
from core.app import app
from fastapi import status
from fastapi.testclient import TestClient


@pytest.fixture(scope="module")
def client():
    return TestClient(app=app)


def test_welcome_route(client: TestClient):
    response = client.get("/")
    response_content = response.json()
    assert response.status_code == status.HTTP_200_OK
    assert (
        response_content["detail"] == f"Welcome to the API from {settings.PROJECT_NAME}"
    )
