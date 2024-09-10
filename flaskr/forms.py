from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField, IntegerField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    new_comment = TextAreaField("New Comment:", validators=[DataRequired()])
    submit_comment = SubmitField("Submit")

class AddItemForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired()])
    description = TextAreaField("Description")
    stock = IntegerField("Stock", validators=[DataRequired()])
    submit = SubmitField("Submit")