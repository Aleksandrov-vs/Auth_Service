import logging
from uuid import UUID
from functools import lru_cache

from src.repositories.role_rep import RoleRepository
from src.models.role import Role


class RoleServices:
    def __init__(self, role_rep: RoleRepository):
        self._repository = role_rep

    def create_role(self, login: str) -> Role:
        new_role = self._repository.create_role(login)
        return new_role

    def delete_role(self, role_id: UUID):
        self._repository.delete_role(role_id)

    def update_role(self, role_id: UUID, name: str) -> Role:
        role = self._repository.update_role(role_id=role_id, name=name)
        return role

    def viewing_role(self, role_id: UUID) -> Role:
        role = self._repository.viewing_role(role_id)
        return role


@lru_cache()
def get_token_service(role_repository: RoleRepository):
    logging.info('init RoleServices')
    return RoleRepository(role_repository)