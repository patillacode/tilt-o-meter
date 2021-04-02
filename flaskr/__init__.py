import os

from flask import Flask, render_template

from . import tiltometer


def error_handler(err):
    return render_template('404.html'), 404


def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=False)
    app.config.from_object(
        os.environ.get('APP_SETTINGS', 'flaskr.config.ProductionConfig')
    )

    # app.register_error_handler(404, error_handler)
    # app.register_error_handler(500, error_handler)

    app.register_blueprint(tiltometer.bp)

    return app
