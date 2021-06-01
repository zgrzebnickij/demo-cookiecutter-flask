from behave import *
from my_flask_app.user.models import User

@given(u'user navigated to {endpoint}')
def navigate_to(context, endpoint):
    context.response = context.client.get(endpoint)
    print(context.response)


@given(u'user "{username}" exists')
def create_user(context, username):
    User(username='jdoe', email='sads').save()


@when(u'fill registration form for user "{username}"')
def step_impl(context, username):
    form = context.response.forms["registerForm"]
    form["username"] = username
    form["email"] = "jdoe@example.com"
    form["password"] = "secret"
    form["confirm"] = "secret"
    context.response = form.submit()

@then(u'registration fails with error "Username already registered"')
def step_impl(context):
    assert "Username already registered" in context.response

@when(u'fill to short password "{password}" in registration form for user "{username}"')
def step_impl(context, username, password):
    form = context.response.forms["registerForm"]
    form["username"] = username
    form["email"] = "jdoe@example.com"
    form["password"] = password
    form["confirm"] = password
    context.response = form.submit()


@then(u'it fails with error "{error}"')
def step_impl(context, error):
    assert error in context.response