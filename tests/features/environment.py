from behave import fixture, use_fixture

from my_flask_app.app import create_app
from my_flask_app.extensions import db
from webtest import TestApp


@fixture
def testapp(context, *args, **kwargs):
    app = create_app('tests.settings')
    app.testing = True
    context.client = TestApp(app)
    with app.app_context():
        db.create_all()
        yield context.client


def before_feature(context, feature):
    use_fixture(testapp, context)