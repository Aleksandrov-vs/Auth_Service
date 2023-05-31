from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

from src.api.v1.hello_controller import hello_bp
from src.core.config import settings


db = SQLAlchemy()
migrate = Migrate()


def create_app():
    app = Flask(__name__)
    app.config['DEBUG'] = settings.debug
    app.config['SECRET_KEY'] = settings.secret_key
    app.register_blueprint(hello_bp)

    # Configure Flask-SQLAlchemy
    app.config["SQLALCHEMY_DATABASE_URI"] = f"postgresql://{settings.postgres.user}:{settings.postgres.password}@" \
                                            f"{settings.postgres.host}:{settings.postgres.port}/{settings.postgres.dbname}"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    
    # Database initialisation
    db.init_app(app)
    migrate.init_app(app, db)

    return app
