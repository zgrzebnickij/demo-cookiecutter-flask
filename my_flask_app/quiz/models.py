# -*- coding: utf-8 -*-
"""User models."""
import json
import datetime as dt

from jsonschema import validate
from my_flask_app.quiz.validation import guestion_schema
from my_flask_app.database import Column, PkModel, db, reference_col, relationship


class Quiz(PkModel):
    """A single quiz"""

    __tablename__ = "quizzes"
    questions = Column(db.String(), unique=True, nullable=False)
    score = Column(db.Integer(), nullable=False)
    created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    user_id = reference_col("users", nullable=False)
    user = relationship("User", backref="quizzes")

    def __init__(self, questions, user_id, **kwargs):
        """Create instance."""
        self.validate_questions(questions)
        score = self.calculate_score(questions)
        super().__init__(questions=json.dumps(questions), score=score, user_id=user_id, **kwargs)

    @property
    def json_question(self):
        """Full user name."""
        return json.loads(self.questions)

    def __repr__(self):
        """Represent instance as a unique string."""
        return f"<Quiz(id={self.id!r}, score={self.score!r}, user_id={self.user_id!r})>"

    @staticmethod
    def validate_questions(questions):
        validate(instance=questions, schema=guestion_schema)

    @staticmethod
    def calculate_score(questions):
        score = 0
        for question in questions['results']:
            if question['answer'] == question['correct_answer']:
                score += 1
        return score
        

