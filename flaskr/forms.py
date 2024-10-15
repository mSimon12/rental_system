from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired, NumberRange

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