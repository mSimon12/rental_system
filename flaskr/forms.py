from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, Email, EqualTo, NumberRange


class LoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')


class RegistrationForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    email = StringField('Email', validators=[DataRequired(), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    password2 = PasswordField('Repeat Password', validators=[DataRequired(), EqualTo('password')])
    submit = SubmitField('Register')


class CommentForm(FlaskForm):
    new_comment = TextAreaField("New Comment:", validators=[DataRequired()])
    submit_comment = SubmitField("Submit")


class AddItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    stock = IntegerField("Stock", validators=[DataRequired(), NumberRange(min=1)])
    submit = SubmitField("Submit")


class RentItemForm(FlaskForm):
    rent_item = SubmitField("Rent")


class ReturnItemForm(FlaskForm):
    return_item = SubmitField("Return")
