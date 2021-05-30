# -*- coding: utf-8 -*-
"""Test forms."""
import json

import pytest

from my_flask_app.public.forms import LoginForm
from my_flask_app.user.forms import RegisterForm
from my_flask_app.quiz.forms import QuizForm


class TestRegisterForm:
    """Register form."""

    def test_validate_user_already_registered(self, user):
        """Enter username that is already registered."""
        form = RegisterForm(
            username=user.username,
            email="foo@bar.com",
            password="example",
            confirm="example",
        )

        assert form.validate() is False
        assert "Username already registered" in form.username.errors

    def test_validate_email_already_registered(self, user):
        """Enter email that is already registered."""
        form = RegisterForm(
            username="unique", email=user.email, password="example", confirm="example"
        )

        assert form.validate() is False
        assert "Email already registered" in form.email.errors

    def test_validate_success(self, db):
        """Register with success."""
        form = RegisterForm(
            username="newusername",
            email="new@test.test",
            password="example",
            confirm="example",
        )
        assert form.validate() is True


class TestLoginForm:
    """Login form."""

    def test_validate_success(self, user):
        """Login successful."""
        user.set_password("example")
        user.save()
        form = LoginForm(username=user.username, password="example")
        assert form.validate() is True
        assert form.user == user

    def test_validate_unknown_username(self, db):
        """Unknown username."""
        form = LoginForm(username="unknown", password="example")
        assert form.validate() is False
        assert "Unknown username" in form.username.errors
        assert form.user is None

    def test_validate_invalid_password(self, user):
        """Invalid password."""
        user.set_password("example")
        user.save()
        form = LoginForm(username=user.username, password="wrongpassword")
        assert form.validate() is False
        assert "Invalid password" in form.password.errors

    def test_validate_inactive_user(self, user):
        """Inactive user."""
        user.active = False
        user.set_password("example")
        user.save()
        # Correct username and password, but user is not activated
        form = LoginForm(username=user.username, password="example")
        assert form.validate() is False
        assert "User not activated" in form.username.errors

class TestQuizForm:
    """Quiz form."""

    def test_validate(self, user, guestions_fake):
        """Enter username that is already registered."""
        form = QuizForm(
            questions=json.dumps(guestions_fake),
            answer_1="blabla",
            answer_2="blabla",
            answer_3="blabla",
            answer_4="blabla",
            answer_5="blabla"
        )
        assert form.validate() is True

    def test_validate_false(self, user, guestions_fake):
        """Enter username that is already registered."""
        form = QuizForm(
            questions=json.dumps(guestions_fake),
            answer_1=1,
            answer_2="blabla",
            answer_3="blabla",
            answer_4=False,
            answer_5="blabla"
        )
        assert form.validate() is False

    def test_validate_missing_field(self, user, guestions_fake):
        """Enter username that is already registered."""
        form = QuizForm(
            questions=json.dumps(guestions_fake),
            answer_1=1,
            answer_2="blabla",
            answer_4=False,
            answer_5="blabla"
        )
        assert form.validate() is False


