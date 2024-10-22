from flask import Blueprint, request, render_template, redirect, url_for
from flaskr.forms import RegistrationForm, LoginForm
from flask_login import UserMixin

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
        return redirect(url_for('main_page'))

    return redirect(url_for('user.login_view'))




