import gevent.monkey
gevent.monkey.patch_all()

from dotenv import load_dotenv

from src import create_app, db

load_dotenv()

app = create_app()
app.app_context().push()


def main():
    app.run()


if __name__ == '__main__':
    main()
