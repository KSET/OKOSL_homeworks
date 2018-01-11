from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileRequired
from wtforms import StringField, SubmitField, TextAreaField
from wtforms.validators import DataRequired


class LoginForm(FlaskForm):
	title = StringField("Title", validators=[DataRequired()])
	author = StringField("Author", validators=[DataRequired()])
	body = TextAreaField("Body", validators=[DataRequired()])
	image = FileField("Image", validators=[FileRequired()])
	submit = SubmitField("Publish")


class CommentForm(FlaskForm):
	author = StringField("Author", validators=[DataRequired()])
	body = TextAreaField("Comment", validators=[DataRequired()])
	submit = SubmitField("Comment")
