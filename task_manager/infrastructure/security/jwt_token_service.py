from __future__ import annotations

from datetime import datetime, timedelta, timezone
from uuid import UUID

import jwt

from task_manager.domain.interfaces.token_service import TokenService


class JWTTokenService(TokenService):
    def __init__(
        self, secret_key: str, algorithm: str = "HS256", expire_minutes: int = 60
    ) -> None:
        self.secret_key = secret_key
        self.algorithm = algorithm
        self.expire_minutes = expire_minutes

    def generate(self, user_id: UUID) -> str:
        payload = {
            "sub": str(user_id),
            "exp": datetime.now(timezone.utc) + timedelta(minutes=self.expire_minutes),
        }
        return jwt.encode(payload, self.secret_key, algorithm=self.algorithm)

    def decode(self, token: str) -> UUID:
        payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
        return UUID(payload["sub"])
