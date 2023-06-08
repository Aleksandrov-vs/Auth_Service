import logging

from flask import Flask
import redis
from flask_jwt_extended import JWTManager
from flask_bcrypt import Bcrypt

from src.api.v1.hello_controller import hello_bp
from src.api.v1.token_controller import token
from src.api.v1.role_controller import role_bp
from src.core.config import settings
from src.models.db import db
from src.models import auth_history
from src.models import role
from src.models import user
from src.models.utils import migrate, security
from src.repositories import token_rep, role_rep
from src.utils.create_superuser import create_superuser


def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['DEBUG'] = settings.debug
    app.config['SECRET_KEY'] = settings.secret_key

    # Configure Flask-SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{settings.postgres.user}:{settings.postgres.password}@" \
                                            f"{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.dbname}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    jwt = JWTManager(app)
    bcrypt = Bcrypt(app)

    redis_db = redis.Redis(host=settings.redis.host, port=settings.redis.port)
    token_rep.token_repository = token_rep.TokenRepository(redis_db, db.session)

    role_rep.role_repository = role_rep.RoleRepository(db.session)

    app.register_blueprint(hello_bp)
    app.register_blueprint(token)
    app.register_blueprint(role_bp)

    #register command
    app.cli.add_command(create_superuser)

    # Database initialization
    db.init_app(app)
    security.init_app(app)
    app.logger.info('Initialized database complete.')

    return app
