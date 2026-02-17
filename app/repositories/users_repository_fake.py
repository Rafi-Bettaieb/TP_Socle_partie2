from __future__ import annotations

from app.repositories.protocols.i_user_repository import IUsersRepository
from typing import Protocol
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate


class FakeUsersRepository(IUsersRepository):
    def __init__(self, factory: IUsersFactory,json_path: str) -> None:
        self._factory = factory
        self._users: list[UserModel] = factory.create_users(json_path)


    def list_users(self) -> list[UserModel]:
        return list(self._users)

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        for u in self._users:
            if u.id == user_id:
                return u
        return None

    def create_user(self, payload: UserModelCreate) -> UserModel:
        next_id = max((u.id for u in self._users), default=0) + 1

        created = UserModel(
            id=next_id,
            login=payload.login,
            age=payload.age,
        )
        self._users.append(created)
        return created
