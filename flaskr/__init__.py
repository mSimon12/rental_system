from flask import Flask
import os

from . import db
from . import store
from . import shelf_manager
from . import clients


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    @app.route("/")
    def main_page():
        return "Welcome!"

    db.init_app(app)

    app.register_blueprint(shelf_manager.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(clients.bp)

    return app
