import gevent.monkey
gevent.monkey.patch_all()

from dotenv import load_dotenv

from src import create_app


load_dotenv()

app = create_app()

for rule in app.url_map.iter_rules():
    print(rule)


def main():
    app.run()


if __name__ == '__main__':
    main()
