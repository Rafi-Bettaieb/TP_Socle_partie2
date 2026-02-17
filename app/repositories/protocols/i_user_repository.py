from __future__ import annotations

from typing import Protocol

from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate

class IUsersRepository(Protocol) :
    def list_users(self) -> list[UserModel]:
        ...

    def get_user(self, user_id: int) -> UserModel | None:
        ...

    def create_user(self, payload: UserModelCreate) -> UserModel:
        ...