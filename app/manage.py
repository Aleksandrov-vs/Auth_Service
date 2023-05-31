import gevent.monkey
gevent.monkey.patch_all()

from flask_migrate import Migrate
from dotenv import load_dotenv

from src import create_app, db

load_dotenv()

app = create_app()
app.app_context().push()

migrate = Migrate(app, db)


def main():
    app.run()


if __name__ == '__main__':
    main()
