import pytest
from backend.settings import settings
from core.contrib.jwt_token import JWTToken


@pytest.fixture(scope="module")
def token_data_access():
    return {"token_type": "access", "sub": "test@test.com"}


@pytest.fixture(scope="module")
def token_data_refresh():
    return {"token_type": "refresh", "sub": "test@test.com"}


def test_access_token(token_data_access):
    jwt = JWTToken()
    token = jwt.create_access_token(token_data_access)

    assert type(token) == str

    token_email = jwt.verify_token(token, "", settings.JWT["JWT_SECRET_KEY"])
    assert token_email.email == token_data_access["sub"]


def test_refresh_token(token_data_refresh):
    jwt = JWTToken()
    token = jwt.create_access_token(token_data_refresh)

    assert type(token) == str

    token_email = jwt.verify_token(token, "", settings.JWT["JWT_REFRESH_SECRET_KEY"])
    assert token_email.email == token_data_refresh["sub"]
