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
    submit_remark = SubmitField("Submit remark")


class FinalRemarkForm(FlaskForm):
    """
    This class defines a form for inputting final remarks. It is structurally identical to RemarkForm, but reusing it
    caused problems with passing data. It should be looked into in the future.
    """

    remark_text = TextAreaField(label="Final remark text", validators=[DataRequired()])
    remark_score_percentage = DecimalField(label="Score percentage", validators=[DataRequired(), NumberRange(min=0, max=1.5)])
    submit_final_remark = SubmitField("Submit final remark")
