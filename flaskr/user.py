from flask import Blueprint, render_template, redirect, url_for, flash
from werkzeug.security import generate_password_hash, check_password_hash
from flaskr.forms import RegistrationForm, LoginForm
from flaskr.api_interface import UserInterface
from flask_login import UserMixin, login_user, logout_user, login_required

bp = Blueprint('user', __name__, url_prefix='/user')


@bp.route('/register')
def register_view():
    register_form = RegistrationForm()
    return render_template('registration.html', title='Register', form=register_form)


@bp.route('/register', methods=['POST'])
def register_request():
    register_form = RegistrationForm()

    if register_form.validate_on_submit():
        # Add here register procedure
        pwd_hash = generate_password_hash(register_form.password.data)

        username = register_form.username.data
        email = register_form.email.data

        call_status = UserInterface.add_user(username, email, pwd_hash)
        if not call_status:
            flash("Not able to add new user!")
        else:
            return redirect(url_for('user.login_view'))

    return redirect(url_for('user.register_view'))


@bp.route('/login')
def login_view():
    login_form = LoginForm()
    return render_template('login.html', title='Login', form=login_form)


@bp.route('/login', methods=['POST'])
def login_request():
    login_form = LoginForm()

    if login_form.validate_on_submit():
        # Add here login authentication
        user = UserInterface.get_user(username=login_form.username.data)
        if check_password_hash(user.password, login_form.password.data):
            login_user(user)

            return redirect(url_for('main_page'))
        else:
            flash("Invalid login data!")

    return redirect(url_for('user.login_view'))


@bp.route("/logout")
@login_required
def logout():
    logout_user()
    return redirect(url_for('main_page'))


def get_user(user_id):
    resp = UserInterface.get_user_info(user_id)
    if resp:
        username = resp['username']
        email = resp['email']
        pwd = resp['password']
        user = User(user_id, username, email, pwd)
        return user

    return None


class User(UserMixin):

    def __init__(self, id, username, email, password):
        self.id = id
        self.username = username
        self.email = email
        self.password = password
