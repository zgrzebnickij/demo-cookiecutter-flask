# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from my_flask_app.database import db
from my_flask_app.user.models import User


class BaseFactory(SQLAlchemyModelFactory):
    """Base factory."""

    class Meta:
        """Factory configuration."""

        abstract = True
        sqlalchemy_session = db.session


class UserFactory(BaseFactory):
    """User factory."""

    username = Sequence(lambda n: f"user{n}")
    email = Sequence(lambda n: f"user{n}@example.com")
    password = PostGenerationMethodCall("set_password", "example")
    active = True

    class Meta:
        """Factory configuration."""

        model = User

class QuizFactory(BaseFactory):
    """ Qiuz factory. """

    # questions = {
    #     "response_code":0,
    #     "results":[
    #         {
    #             "category":"Category 1",
    #             "type":"multiple",
    #             "difficulty":"medium",
    #             "question": f"question {n}",
    #             "correct_answer":"answer 1",
    #             "incorrect_answers":[
    #                 "answer 2",
    #                 "answer 3",
    #                 "answer 4"
    #             ]
    #         } for n in range(5)
    #     ]
    # }
    # created_at = Column(db.DateTime, nullable=False, default=dt.datetime.utcnow)
    # user_id = reference_col("users", nullable=True)
    # user = relationship("User", backref="quizzes")