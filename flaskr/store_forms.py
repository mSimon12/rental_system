from flask_wtf import FlaskForm
from wtforms import TextAreaField, SubmitField
from wtforms.validators import DataRequired

class CommentForm(FlaskForm):
    new_comment = TextAreaField("New Comment:", validators=[DataRequired()])
    submit_comment = SubmitField("Submit")