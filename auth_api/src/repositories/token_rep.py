import datetime
import logging
import uuid

from redis import Redis
from uuid import UUID

from src.models.auth_history import AuthHistory
from src.models.role import Role
from src.models.user import User
from flask_sqlalchemy import session

from typing import Union


class TokenRepository:

    def __init__(self, redis_cli: Redis, db_session: session):
        self._redis = redis_cli
        self._postgres_session = db_session

    def _set(self, key: str, expire: Union[int, float], value: Union[str, int]):
        self._redis.setex(key, expire, value)

    def _get(self, value):
        return self._redis.get(value)

    def user_is_exist(self, login: str):
        existing_user = User.query.filter_by(login=login).first()
        logging.warning(existing_user)
        if existing_user:
            return True
        return False

    def get_user_by_id(self, user_id: UUID) -> User:
        user = User.query.filter_by(id=user_id).first()
        return user

    def get_user_by_login(self, login: str) -> User:
        user = User.query.filter_by(login=login).first()
        return user

    def get_user_by_refresh(self, refresh_token: str) -> User:
        user_id = self._get(refresh_token)
        return self.get_user_by_id(user_id)

    def save_token(self, user_id: UUID, new_token: str, new_token_exp:  datetime.timedelta):
        self._set(new_token, new_token_exp, str(user_id))

    def delete_refresh(self, refresh_for_del: str):
        self._redis.delete(refresh_for_del)

    def rework_refresh(
            self, user_id: UUID,
            old_refresh: str, new_refresh: str,
            new_refresh_exp: datetime.timedelta
    ):
        pipeline = self._redis.pipeline()
        pipeline.setex(new_refresh, new_refresh_exp, str(user_id))
        pipeline.delete(old_refresh)
        pipeline.execute()

    def save_new_user(self, login, pass_hash: bytes) -> UUID:
        logging.info(type(pass_hash))
        consumer_role = Role.query.filter_by(name='consumer').first()
        new_user = User(login=login, password=pass_hash)
        new_user.roles.append(consumer_role)
        self._postgres_session.add(new_user)
        self._postgres_session.commit()
        return new_user.id

    def save_login_history(self, user_id: UUID, user_agent: str, auth_date: datetime.datetime):
        new_login = AuthHistory(user_id=user_id, user_agent=user_agent, auth_date=auth_date)
        self._postgres_session.add(new_login)
        self._postgres_session.commit()


token_repository: Union[TokenRepository,  None] = None


def get_token_repository():
    return token_repository
