from datetime import timedelta
import json
import logging
from functools import lru_cache
from http import HTTPStatus
from typing import Tuple

from src.repositories.token_rep import TokenRepository
from src.utils.extensions import create_hash, create_tokens, check_password


class TokenServices:
    def __init__(self, token_rep: TokenRepository):
        self._repository = token_rep

    def change_password(self):
        return 'change-password'

    def login(self, login: str, response_password: str):
        if not self._repository.user_is_exist(login):
            return HTTPStatus.NOT_FOUND, "пользователь с таким логином нет"
        user = self._repository.get_user_by_login(login)
        if not check_password(response_password, user.password):
            return HTTPStatus.NOT_FOUND, "пароль не верный"

        access_exp = timedelta(hours=2)
        access_token, refresh_token = create_tokens(
            identity=json.dumps({'role': 'consumer'}),
            access_expires_delta=access_exp,
        )
        self._repository.save_token(user.id, access_token, access_exp)
        self._repository.save_token(user.id, access_token, access_exp)
        return HTTPStatus.OK, {'access_token': access_token, 'refresh_token': refresh_token}

    def logout(self):
        return 'logout'

    def refresh_tokens(self):
        return 'refresh-tokens'

    def register(self, login: str, password: str) -> Tuple[int, any]:
        if self._repository.user_is_exist(login):
            return HTTPStatus.CONFLICT, "пользователь уже создан"
        pass_hash = create_hash(password)
        user_id = self._repository.save_new_user(login, pass_hash)
        access_exp = timedelta(hours=2)
        access_token, refresh_token = create_tokens(
            identity=json.dumps({'role': 'consumer'}),
            access_expires_delta=access_exp,
        )
        self._repository.save_token(user_id, access_token, access_exp)
        self._repository.save_token(user_id, access_token, access_exp)
        return HTTPStatus.OK, {'access_token': access_token, 'refresh_token': refresh_token}


@lru_cache()
def get_token_service(token_repository: TokenRepository):
    logging.info('init TokenServices')
    return TokenServices(token_repository)
