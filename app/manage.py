import gevent.monkey
gevent.monkey.patch_all()

from dotenv import load_dotenv

from src import create_app
from src.models.db import db


load_dotenv()

app = create_app()
# app.app_context().push()


def main():
    # db.create_all()
    app.run()


if __name__ == '__main__':
    main()
