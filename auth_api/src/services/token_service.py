import hashlib
import logging
import os
from functools import lru_cache

from src.repositories.token_rep import TokenRepository


class TokenServices:
    def __init__(self, token_rep: TokenRepository):
        self._repository = token_rep

    def change_password(self):
        return 'change-password'

    def login(self):
        return 'login'

    def logout(self):
        return 'logout'

    def refresh_tokens(self):
        return 'refresh-tokens'

    def register(self, login: str, password: str):
        logging.info(self._repository)
        if not self._repository.user_is_exist(login):
            salt = os.urandom(32)
            key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, 100000)
            pass_hash = salt + b":" + key
            self._repository.save_new_user(login, pass_hash)
        return 'register'


@lru_cache()
def get_token_service(token_repository: TokenRepository):
    logging.info('init TokenServices')
    return TokenServices(token_repository)
