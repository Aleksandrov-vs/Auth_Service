import uuid

from redis import Redis
from uuid import UUID

from src.models.role import Role
from src.models.user import User
from flask_sqlalchemy import session

from typing import Union


class TokenRepository:

    def __init__(self, redis_cli: Redis, db_session: session):
        self._redis = redis_cli
        self._postgres_session = db_session

    def _set(self, key: str, expire: int, value: Union[str, int]):
        self._redis.setex(key, expire, value)

    def _get(self, value):
        return self._redis.get(value)

    def user_is_exist(self, login: str):
        print(len(User.query.filter_by(login=login)))

    def get_user_id_by_refresh(self, refresh_token: str) -> UUID:
        user_id = self._get(refresh_token)
        return UUID(user_id)

    def save_refresh(self, user_id: UUID, new_refresh: str, new_refresh_exp: int):
        self._set(new_refresh, new_refresh_exp, str(user_id))

    def delete_refresh(self, refresh_for_del: str):
        self._redis.delete(refresh_for_del)

    def rework_refresh(self, user_id: UUID, old_refresh: str, new_refresh: str, new_refresh_exp: int):
        pipeline = self._redis.pipeline()
        pipeline.setex(new_refresh, new_refresh_exp, str(user_id))
        pipeline.delete(old_refresh)
        pipeline.execute()

    def save_new_user(self, login, pass_hash):
        consumer_role = Role.query.filter_by(name='consumer').first()
        new_user = User(login=login, password=pass_hash, role=consumer_role)
        self._postgres_session.add(new_user)
        self._postgres_session.commit()


token_repository: Union[TokenRepository,  None] = None


def get_token_repository():
    return token_repository
