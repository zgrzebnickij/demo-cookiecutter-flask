  # -*- coding: utf-8 -*-
"""Quiz forms."""
from flask_wtf import FlaskForm
from wtforms import PasswordField, StringField, HiddenField
from wtforms.validators import DataRequired, Email, EqualTo, Length


class QuizForm(FlaskForm):
    """Register form."""

    questions = HiddenField("Questions", validators=[DataRequired()])
    answer_1 = StringField(
        "Answer 1", validators=[DataRequired()]
    )
    answer_2 = StringField(
        "Answer 2", validators=[DataRequired()]
    )
    answer_3 = StringField(
        "Answer 3", validators=[DataRequired()]
    )
    answer_4 = StringField(
        "Answer 4", validators=[DataRequired()]
    )
    answer_5 = StringField(
        "Answer 5", validators=[DataRequired()]
    )

    def __init__(self, *args, **kwargs):
        """Create instance."""
        super(QuizForm, self).__init__(*args, **kwargs)
        self.user = None

    def validate(self):
        """Validate the form."""
        initial_validation = super(QuizForm, self).validate()
        if not initial_validation:
            return False
        return True
