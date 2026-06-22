from task_manager.infrastructure.security.bcrypt_password_hasher import (
    BcryptPasswordHasher,
)


def test_hash_and_verify_round_trip():
    hasher = BcryptPasswordHasher()
    hashed = hasher.hash("s3cret")

    assert hashed != "s3cret"
    assert hasher.verify("s3cret", hashed) is True


def test_verify_rejects_wrong_password():
    hasher = BcryptPasswordHasher()
    hashed = hasher.hash("s3cret")

    assert hasher.verify("wrong", hashed) is False
