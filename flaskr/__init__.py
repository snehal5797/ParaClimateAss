import os

from flask import Flask


def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True)

    from . import auth
    app.register_blueprint(auth.bp)
    app.add_url_rule('/', endpoint='index')

    return app
