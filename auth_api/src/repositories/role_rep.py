from redis import Redis
from uuid import UUID

from src.models.role import Role
from flask_sqlalchemy import session


class RoleRepository:

    def __init__(self, db_session: session):
        self._postgres_session = db_session

    def create_role(self, login: str) -> Role:
        """Создать роль."""
        new_role = Role(name=login)
        self._postgres_session.add(new_role)
        self._postgres_session.commit()
        return new_role

    def delete_role(self, role_id: UUID) -> None:
        """Удалить роль."""
        if Role.query.filter_by(id=role_id).delete():
            self._postgres_session.commit()
        else:
            'Role does not exists.'

    def update_role(self, role_id: UUID, name: str) -> Role:
        """Обновление роли."""
        role = Role.query.filter_by(id=role_id)
        role.name = name
        self._postgres_session.commit()
        return role

    def viewing_role(self, role_id: UUID) -> Role:
        """Просмотр роли."""
        role = Role.query.filter_by(id=role_id).first()
        if not role:
            return 'No role was found'
        return role


role_repository: RoleRepository | None = None


def get_role_repository():
    return role_repository
