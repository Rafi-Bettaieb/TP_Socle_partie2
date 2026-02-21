from __future__ import annotations

from sqlalchemy.orm import Session

from app.models_orm.user_table import UserTable
from app.repositories.protocols.i_user_repository import IUsersRepository
from app.models.user_model import UserModel
from app.models.user_model_create import UserModelCreate


class UsersRepositorySql(IUsersRepository):
    def __init__(self, db:Session) -> None:
        self._db = db

    def list_users(self) -> list[UserModel]:
        return self._db.query(UserTable).all()

    def get_user_by_id(self, user_id: int) -> UserModel | None:
        return self._db.query(UserTable).filter(UserTable.id == user_id).first()

    def create_user(self, payload: UserModelCreate) -> UserModel:
        new_user = UserTable(
            login=payload.login, 
            age=payload.age
        )
        self._db.add(new_user)
        self._db.commit()
        self._db.refresh(new_user)
        return new_user
