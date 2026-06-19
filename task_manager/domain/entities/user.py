from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from uuid import UUID


@dataclass
class User:
    id: UUID
    email: str
    hashed_password: str
    name: str
    created_at: datetime
    is_active: bool = True

    def __post_init__(self) -> None:
        if "@" not in self.email:
            raise ValueError("invalid email")
        if not self.name.strip():
            raise ValueError("name must not be empty")

    def deactivate(self) -> None:
        self.is_active = False
