# -*- coding: utf-8 -*-
"""Defines fixtures available to all tests."""

import logging
import json
import requests

import pytest
from webtest import TestApp

from my_flask_app.quiz import utils
from my_flask_app.app import create_app
from my_flask_app.database import db as _db

from .factories import UserFactory, QuizFactory


@pytest.fixture
def app():
    """Create application for the tests."""
    _app = create_app("tests.settings")
    _app.logger.setLevel(logging.CRITICAL)
    ctx = _app.test_request_context()
    ctx.push()

    yield _app

    ctx.pop()


@pytest.fixture
def testapp(app):
    """Create Webtest app."""
    return TestApp(app)


@pytest.fixture
def db(app):
    """Create database for the tests."""
    _db.app = app
    with app.app_context():
        _db.create_all()

    yield _db

    # Explicitly close DB connection
    _db.session.close()
    _db.drop_all()


@pytest.fixture
def user(db):
    """Create user for the tests."""
    user = UserFactory(password="myprecious")
    db.session.commit()
    return user

@pytest.fixture
def guestions_fake():
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
    return questions

@pytest.fixture
def fake_question_for_user(db, user):
    quiz = QuizFactory(user_id=user.id)
    print(quiz)
    quiz.save()
    db.session.commit()
    return quiz


@pytest.fixture
def mock_response(monkeypatch):
    """Requests.get() mocked to return {'mock_key':'mock_response'}."""

    def mock_get(*args, **kwargs):
        return json.load('/tests/external_api_response.json')

    monkeypatch.setattr(utils, "get_questions_from_API", mock_get)
