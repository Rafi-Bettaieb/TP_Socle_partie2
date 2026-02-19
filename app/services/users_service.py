from __future__ import annotations
from app.repositories.protocols.i_user_repository import IUsersRepository
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate


class UsersService:

    def __init__(self, repository : IUsersRepository) -> None:
        self._repository = repository

    def list_users(self) -> list[UserModel]:
        return self._repository.list_users()

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        return self._repository.get_user_by_id(user_id)

    def create_user(self, payload: UserModelCreate) -> UserModel:
       return self._repository.create_user(payload)
