from flask import Flask, render_template, redirect, url_for, request
from dotenv import load_dotenv
import os
import base64
import json

from flaskr.api_interface import UserInterface
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
        return redirect(url_for('store.store'))

    # Add frontend views
    app.register_blueprint(shelf_manager.bp)
    app.register_blueprint(store.bp)
    app.register_blueprint(user.bp)

    app.context_processor(inject_user_data)

    return app


def inject_user_data():
    token = request.cookies.get("access_token_cookie")
    username = None
    is_admin = False
    user_logged_in = False

    users_interface = UserInterface()
    users_interface.set_token(token)

    if token:
        # Your custom verification logic or request to auth service
        payload = token.split(sep='.')[1]
        client_id = int(json.loads(base64.b64decode(payload))['sub'])
        user_data = users_interface.get_user_by_id(client_id)  # e.g., call to your backend service

        if user_data:
            username = user_data.get("username")
            user_role = user_data.get("role")
            is_admin = user_role == "Admin"
            user_logged_in = True

    return dict(
        user_logged_in=user_logged_in,
        username=username,
        is_admin=is_admin
    )