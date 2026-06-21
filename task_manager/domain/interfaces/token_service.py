from __future__ import annotations

from abc import ABC, abstractmethod
from uuid import UUID


class TokenService(ABC):
    @abstractmethod
    def generate(self, user_id: UUID) -> str:
        ...
