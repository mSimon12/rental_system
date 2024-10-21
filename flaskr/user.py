
from flask import Blueprint, request, render_template, redirect, url_for
from flaskr.forms import RegistrationForm


bp = Blueprint('user', __name__, url_prefix='/user')

@bp.route('/register')
def register():
    register_form = RegistrationForm()
    return render_template('registration.html', title='Register', form=register_form)