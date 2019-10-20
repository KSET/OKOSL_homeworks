from flask_wtf import FlaskForm
from wtforms import TextAreaField, DecimalField, SubmitField
from wtforms.validators import DataRequired, NumberRange


class RemarkForm(FlaskForm):
    """
    This class defines a form for inputting remarks. The form contains the remark's text and its score percentage.
    The author, date and solution group do not have their fields because they can be inferred from the context.
    """

    remark_text = TextAreaField(label="Remark text", validators=[DataRequired()])
    remark_score_percentage = DecimalField(label="Score percentage", validators=[DataRequired(), NumberRange(min=0, max=1.5)])
    submit = SubmitField("Submit remark")
