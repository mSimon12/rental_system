from flask import Blueprint, render_template, redirect, url_for, flash
from flaskr.frontend.forms import RegistrationForm, LoginForm
from flask_login import current_user
from flaskr.frontend.api_interface import UserInterface

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
        username = register_form.username.data
        email = register_form.email.data
        password = register_form.password.data

        call_status = UserInterface.add_user(username, email, password)
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
        username = login_form.username.data
        password = login_form.password.data

        call_status = UserInterface.login_user(username, password)
        if call_status:
            return redirect(url_for('main_page'))
        else:
            flash("Invalid login data!")

    return redirect(url_for('user.login_view'))


@bp.route("/logout")
def logout():
    UserInterface.logout_user(current_user.id)
    return redirect(url_for('main_page'))