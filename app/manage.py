from flask_migrate import Migrate

from dotenv import load_dotenv

load_dotenv()

from src import create_app, db

app = create_app()

app.app_context().push()

migrate = Migrate(app, db)

if __name__ == '__main__':
    app.run()
