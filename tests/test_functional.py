# -*- coding: utf-8 -*-
"""Functional tests using WebTest.

See: http://webtest.readthedocs.org/
"""
from unittest import TestCase
from flask import url_for
from flask_login import current_user, login_required, login_user, logout_user
from my_flask_app.user.models import User
from webtest.app import AppError
from random import choice

from .factories import UserFactory


class TestLoggingIn:
    """Login."""

    def test_can_log_in_returns_200(self, user, testapp):
        """Login successful."""
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "myprecious"
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_sees_alert_on_log_out(self, user, testapp):
        """Show alert on logout."""
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "myprecious"
        # Submits
        res = form.submit().follow()
        res = testapp.get(url_for("public.logout")).follow()
        # sees alert
        assert "You are logged out." in res

    def test_sees_error_message_if_password_is_incorrect(self, user, testapp):
        """Show error if password is incorrect."""
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "wrong"
        # Submits
        res = form.submit()
        # sees error
        assert "Invalid password" in res

    def test_sees_error_message_if_username_doesnt_exist(self, user, testapp):
        """Show error if username doesn't exist."""
        # Goes to homepage
        res = testapp.get("/")
        # Fills out login form, password incorrect
        form = res.forms["loginForm"]
        form["username"] = "unknown"
        form["password"] = "myprecious"
        # Submits
        res = form.submit()
        # sees error
        assert "Unknown user" in res


class TestRegistering:
    """Register a user."""

    def test_can_register(self, user, testapp):
        """Register a new user."""
        old_count = len(User.query.all())
        # Goes to homepage
        res = testapp.get("/")
        # Clicks Create Account button
        res = res.click("Create account")
        # Fills out the form
        form = res.forms["registerForm"]
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["password"] = "secret"
        form["confirm"] = "secret"
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200
        # A new user was created
        assert len(User.query.all()) == old_count + 1

    def test_sees_error_message_if_passwords_dont_match(self, user, testapp):
        """Show error if passwords don't match."""
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but passwords don't match
        form = res.forms["registerForm"]
        form["username"] = "foobar"
        form["email"] = "foo@bar.com"
        form["password"] = "secret"
        form["confirm"] = "secrets"
        # Submits
        res = form.submit()
        # sees error message
        assert "Passwords must match" in res

    def test_sees_error_message_if_user_already_registered(self, user, testapp):
        """Show error if user already registered."""
        user = UserFactory(active=True)  # A registered user
        user.save()
        # Goes to registration page
        res = testapp.get(url_for("public.register"))
        # Fills out form, but username is already registered
        form = res.forms["registerForm"]
        form["username"] = user.username
        form["email"] = "foo@bar.com"
        form["password"] = "secret"
        form["confirm"] = "secret"
        # Submits
        res = form.submit()
        # sees error
        assert "Username already registered" in res

class TestQuiz:
    """Register a user."""

    def test_get_quiz_not_logged(self, user, testapp):
        """Register a new quiz"""
        try:
            res = testapp.get("/quiz/")
            assert False, 'App should return 401 UNAUTHORIZED' 
        except AppError as err:
            print(dir(err))
            assert '401 UNAUTHORIZED' in str(err), 'fApp should return 401 UNAUTHORIZED, but got {err}' 

    def test_save_Quiz(self, user, testapp):
        """Register a new quiz"""
        # (the test case is within a test request context)
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "myprecious"
        # Submits
        res = form.submit().follow()
        
        res = testapp.get("/quiz/")
        # Fills out the form
        form = res.forms["quizForm"]
        for index in range(1,6):
            print(form['answer_1'].options)
            form[f"answer_{index}"] = choice(form[f'answer_{index}'].options)[0]
        # Submits
        res = form.submit().follow()
        assert res.status_code == 200

    def test_get_quiz(self, user, testapp, fake_question_for_user):
        """Register a new quiz"""
        # (the test case is within a test request context)
        res = testapp.get("/")
        # Fills out login form in navbar
        form = res.forms["loginForm"]
        form["username"] = user.username
        form["password"] = "myprecious"
        # Submits
        res = form.submit().follow()
        print(fake_question_for_user)
        res = testapp.get(f"/quiz/{fake_question_for_user.id}")
        assert res.status_code == 200

    def test_get_quiz_scores(self, user, testapp, fake_question_for_user):
        """Register a new quiz"""
        res = testapp.get(f"/quiz/quizzes")
        assert res.status_code == 200
        assert res.html.find(id="scoreboard"), 'No div with id=scoreboard'



        
        