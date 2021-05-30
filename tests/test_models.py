# -*- coding: utf-8 -*-
"""Model unit tests."""
import datetime as dt

import pytest
from jsonschema import ValidationError

from my_flask_app.user.models import Role, User
from my_flask_app.quiz.models import Quiz

from .factories import UserFactory


@pytest.mark.usefixtures("db")
class TestUser:
    """User tests."""

    def test_get_by_id(self):
        """Get user by ID."""
        user = User("foo", "foo@bar.com")
        user.save()

        retrieved = User.get_by_id(user.id)
        assert retrieved == user

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert bool(user.created_at)
        assert isinstance(user.created_at, dt.datetime)

    def test_password_is_nullable(self):
        """Test null password."""
        user = User(username="foo", email="foo@bar.com")
        user.save()
        assert user.password is None

    def test_factory(self, db):
        """Test user factory."""
        user = UserFactory(password="myprecious")
        db.session.commit()
        assert bool(user.username)
        assert bool(user.email)
        assert bool(user.created_at)
        assert user.is_admin is False
        assert user.active is True
        assert user.check_password("myprecious")

    def test_check_password(self):
        """Check password."""
        user = User.create(username="foo", email="foo@bar.com", password="foobarbaz123")
        assert user.check_password("foobarbaz123") is True
        assert user.check_password("barfoobaz") is False

    def test_full_name(self):
        """User full name."""
        user = UserFactory(first_name="Foo", last_name="Bar")
        assert user.full_name == "Foo Bar"

    def test_roles(self):
        """Add a role to a user."""
        role = Role(name="admin")
        role.save()
        user = UserFactory()
        user.roles.append(role)
        user.save()
        assert role in user.roles

@pytest.mark.usefixtures("db")
class TestSingleQuiz:
    """Quiz tests."""

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
                "answer": "answer 1"
            } for n in range(5)
        ]
    }

    def test_quiz_model(self):
        try:
            from my_flask_app.quiz.models import Quiz
        except ImportError:
            assert False, 'No Quiz model in quiz models'


    def test_get_by_id(self):
        """Get test by ID."""
        quiz = Quiz(self.questions, 6)
        quiz.save()

        retrieved = Quiz.get_by_id(quiz.id)
        assert retrieved == quiz

    def test_created_at_defaults_to_datetime(self):
        """Test creation date."""
        quiz = Quiz(self.questions, 5)
        quiz.save()
        assert bool(quiz.created_at)
        assert isinstance(quiz.created_at, dt.datetime)

    def test_correct_question(self):
        quiz = Quiz(self.questions, 4)
        quiz.save()

        retrieved = Quiz.get_by_id(quiz.id)
        print(retrieved)
        assert retrieved.questions == quiz.questions, f'question should be {self.questions}'

    def test_validate_question_structure(self):
        question = {'testquiz': 'answer'}
        with pytest.raises(ValidationError):
            Quiz(question, 3)

    def test_calculation_of_score(self):
        quiz = Quiz(self.questions, 2)
        quiz.save()
        assert quiz.score == 5

    def test_correct_user_id(self):
        quiz = Quiz(self.questions, 7)
        quiz.save()
        assert quiz.user_id == 7
