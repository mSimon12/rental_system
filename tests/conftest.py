import os
import tempfile
import pytest
from flaskr import create_app
from flaskr.api.db import get_db, init_db
from werkzeug.security import generate_password_hash
import json

with open(os.path.join(os.path.dirname(__file__), 'data.sql'), 'rb') as f:
    _data_sql = f.read().decode('utf8')


@pytest.fixture
def app():
    db_fd, db_path = tempfile.mkstemp()

    app = create_app({
        'TESTING': True,
        'DATABASE': db_path,
    })

    with app.app_context():
        init_db()
        db = get_db()
        db.executescript(_data_sql)

        with open("tests/test_vars.json", "r") as test_file:
            test_vars = json.load(test_file)

        for user in test_vars['users'].values():
            db.execute(
                "INSERT INTO users (username, email, password, role_id) VALUES (?,?,?,?)",
                (user['username'], user['email'], generate_password_hash(user['password']), user['role_id'])
            )
            db.commit()


    yield app

    os.close(db_fd)
    os.unlink(db_path)


@pytest.fixture
def api_client(app):
    return app.test_client()


@pytest.fixture
def runner(app):
    return app.test_cli_runner()
