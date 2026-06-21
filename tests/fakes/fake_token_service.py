from __future__ import annotations

from uuid import UUID

from task_manager.domain.interfaces.token_service import TokenService


class FakeTokenService(TokenService):
    def generate(self, user_id: UUID) -> str:
        return f"token-for-{user_id}"
