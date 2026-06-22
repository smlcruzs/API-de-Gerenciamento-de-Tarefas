from __future__ import annotations

from uuid import UUID

from task_manager.domain.interfaces.token_service import TokenService


class FakeTokenService(TokenService):
    PREFIX = "token-for-"

    def generate(self, user_id: UUID) -> str:
        return f"{self.PREFIX}{user_id}"

    def decode(self, token: str) -> UUID:
        if not token.startswith(self.PREFIX):
            raise ValueError("invalid token")
        return UUID(token.removeprefix(self.PREFIX))
