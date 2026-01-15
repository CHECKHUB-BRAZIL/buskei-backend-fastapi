import pytest
from fastapi.testclient import TestClient
from app.infra.redis.dependencies import get_redis
from app.main import app

from app.modules.auth.infrastructure.security.jwt_handler import JWTHandler
from tests.fakes.fake_redis import FakeRedis




@pytest.fixture
def fake_redis():
    return FakeRedis()


@pytest.fixture
def client(fake_redis):
    app.dependency_overrides[get_redis] = lambda: fake_redis
    yield TestClient(app)
    app.dependency_overrides.clear()


@pytest.fixture
def valid_access_token():
    jwt = JWTHandler()
    return jwt.create_access_token("user-id-test")
