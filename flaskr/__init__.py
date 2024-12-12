from flask import Flask, render_template
from dotenv import load_dotenv
import os
from flask_login import LoginManager
from flask_jwt_extended import JWTManager

# Backend
from flaskr.api import db
from flaskr.api.controllers import users
from flaskr.api.controllers import items
from flaskr.api.services.users import UsersService

# Frontend
from flaskr.frontend import user, store, shelf_manager


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)

    load_dotenv()

    app.config.from_mapping(
        SECRET_KEY= os.getenv("API_SECRET"),
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'),
    )

    jwt = JWTManager(app)

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

    db.init_app(app)

    login_manager = LoginManager()
    # login_manager.login_view = 'user.login_view'
    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(user_id):
        return UsersService.get_user(user_id)

    # Add store API
    app.register_blueprint(items.bp)
    app.register_blueprint(users.bp)

    # Add frontend views
    app.register_blueprint(shelf_manager.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(user.bp)

    return app
