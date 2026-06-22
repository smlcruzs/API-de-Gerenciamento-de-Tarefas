from __future__ import annotations

from task_manager.domain.interfaces.password_hasher import PasswordHasher


class FakePasswordHasher(PasswordHasher):
    PREFIX = "hashed:"

    def hash(self, plain_password: str) -> str:
        return f"{self.PREFIX}{plain_password}"

    def verify(self, plain_password: str, hashed_password: str) -> bool:
        return hashed_password == self.hash(plain_password)
