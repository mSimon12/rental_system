from flask import Flask, render_template
from dotenv import load_dotenv
import os

from . import user, store, shelf_manager


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    load_dotenv()

    app.config.from_mapping(
        SECRET_KEY= os.getenv("API_SECRET"),
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
        return render_template("base.html")

    # Add frontend views
    app.register_blueprint(shelf_manager.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(user.bp)

    return app
