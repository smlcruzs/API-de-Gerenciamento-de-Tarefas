from uuid import uuid4

import jwt
import pytest

from task_manager.infrastructure.security.jwt_token_service import JWTTokenService


def test_generate_and_decode_round_trip():
    service = JWTTokenService(secret_key="test-secret")
    user_id = uuid4()

    token = service.generate(user_id)

    assert service.decode(token) == user_id


def test_decode_rejects_token_signed_with_different_secret():
    service = JWTTokenService(secret_key="test-secret")
    other_service = JWTTokenService(secret_key="other-secret")
    token = service.generate(uuid4())

    with pytest.raises(jwt.InvalidTokenError):
        other_service.decode(token)


def test_decode_rejects_expired_token():
    service = JWTTokenService(secret_key="test-secret", expire_minutes=-1)
    token = service.generate(uuid4())

    with pytest.raises(jwt.ExpiredSignatureError):
        service.decode(token)
