from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired

class PostForm(FlaskForm):
    joke = TextAreaField("Text", validators=[DataRequired()])
    submit = SubmitField("Submit")