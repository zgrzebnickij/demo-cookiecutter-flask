# -*- coding: utf-8 -*-
"""Factories to help in tests."""
from factory import PostGenerationMethodCall, Sequence
from factory.alchemy import SQLAlchemyModelFactory

from my_flask_app.database import db
from my_flask_app.user.models import User
from my_flask_app.quiz.models import Quiz

import json


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

    questions = {
        "response_code":0,
        "results":[
            {
                "category":"Category 1",
                "type":"multiple",
                "difficulty":"medium",
                "question": f"question {n}",
                "correct_answer":"answer 1",
                "incorrect_answers":[
                    "answer 2",
                    "answer 3",
                    "answer 4"
                ],
                "answer": "answer_4",
            } for n in range(5)
        ]
    }

    class Meta:
        """Factory configuration."""

        model = Quiz