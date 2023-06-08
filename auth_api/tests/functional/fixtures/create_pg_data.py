import bcrypt
import pytest
import pytest_asyncio
import sqlalchemy
from sqlalchemy import create_engine, text

from functional.settings import test_settings


@pytest.fixture(scope='session')
def pg_engine():
    engine = create_engine(f"postgresql://{test_settings.pg_user}:"
                           f"{test_settings.pg_password}@{test_settings.pg_host}"
                           f":{test_settings.pg_port}/{test_settings.dbname}")
    yield engine


@pytest.fixture(scope="session", autouse=True)
def delete_all_pg_data(pg_engine: sqlalchemy.Engine):
    def delete(engine):
        table_names = [
            "auth_history",
            "user_role",
            "roles",
            "users",
        ]

        with engine.begin() as connection:
            for table in table_names:
                query = text(f"TRUNCATE {table} RESTART IDENTITY CASCADE;")
                connection.execute(
                    query
                )

    delete(pg_engine)
    yield
    delete(pg_engine)


@pytest_asyncio.fixture(scope="session")
async def admin_tokens(make_get_request, pg_engine: sqlalchemy.Engine):
    test_user_login = 'test_admin'
    test_user_password = 'test_admin'
    salt = bcrypt.gensalt()
    test_user_password = test_user_password.encode('utf-8')
    hashed_password = bcrypt.hashpw(test_user_password, salt)
    requests = [
        f"INSERT INTO users(id, login, password) VALUES ('8c459f2a-9427-42c9-9058-dc6b0abd220a', :login, :password);",
        f"INSERT INTO roles(id, name) VALUES ('4c0b16c7-8095-4701-b80e-1cd10db6eac7', 'admin');",
        f"INSERT INTO user_role(id, user_id, role_id) VALUES ('73734f1d-8861-46a7-9506-02ceb0713806', '8c459f2a-9427-42c9-9058-dc6b0abd220a', '4c0b16c7-8095-4701-b80e-1cd10db6eac7');"
    ]
    with pg_engine.begin() as connection:
        for query in requests:
            connection.execute(
                text(query),
                {"login": test_user_login, "password": hashed_password}
            )

    reg_body, reg_status = await make_get_request(
        test_settings.service_url + '/api/v1/auth/login',
        method='POST',
        data={'login': 'test_admin', 'password': 'test_admin'}
    )
    yield reg_body
