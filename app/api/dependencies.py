"""
Module de composition de l'application.

Rôle :
- Lire la configuration (Settings)
- Choisir l'implémentation du repository
- Construire le service
- Exposer une dépendance FastAPI unique
"""

from fastapi import Depends
from sqlalchemy.orm import Session

from app.core.settings import get_settings
from app.db.session import get_db

from app.repositories.protocols.i_user_repository import IUsersRepository
from app.repositories.users_repository_fake import FakeUsersRepository
from app.repositories.users_repository_sql import UsersRepositorySql

from app.factories.users_factory import UsersFactory
from app.services.users_service import UsersService


# ----------------------------------------------------------------------
# 1. Factory de repository
# ----------------------------------------------------------------------

def build_users_repository(
    settings,
    db: Session | None = None,
) -> IUsersRepository:
    """
    Construit le repository Users en fonction de la configuration.
    """
    
    if settings.users_backend == "fake":
        factory = UsersFactory()
        return FakeUsersRepository(factory=factory, json_path=settings.users_json_path)
        
    elif settings.users_backend == "db":
        if db is None:
            raise RuntimeError("Une session de base de données (db) est requise pour le backend 'db'")
        return UsersRepositorySql(db)
        
    else:
        raise ValueError(f"Backend non supporté : {settings.users_backend}")


# ----------------------------------------------------------------------
# 2. Fournisseur UNIQUE de service
# ----------------------------------------------------------------------

def get_users_service(
    settings=Depends(get_settings),
    db: Session = Depends(get_db),
) -> UsersService:
    """
    Dépendance FastAPI principale.
    """
    
    repo = build_users_repository(settings, db=db)
    
    return UsersService(repo)