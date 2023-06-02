import logging

from flask import Flask

from src.api.v1.hello_controller import hello_bp
from src.core.config import settings
from src.models.db import db
from src.models.utils import migrate, security


def create_app():
    app = Flask(__name__)

    # App configuration
    app.config['DEBUG'] = settings.debug
    app.config['SECRET_KEY'] = settings.secret_key

    # Configure Flask-SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{settings.postgres.user}:{settings.postgres.password}@" \
                                            f"{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.dbname}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    app.register_blueprint(hello_bp)
    
    # Database initialization
    db.init_app(app)
    migrate.init_app(app, db)
    security.init_app(app)
    app.logger.info('Initialized database complete.')

    return app
