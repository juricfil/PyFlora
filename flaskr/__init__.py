import os
from flask import Flask
from . import db, auth, home, plants


def create_app(test_config=None):
    """
    Creates webapp from blueprints, tako test_config if running test on the app.
    """
    app = Flask(__name__, instance_relative_config=True)  # creates app
    app.config.from_mapping(
        SECRET_KEY="dev",
        SQLALCHEMY_DATABASE_URI="sqlite:///"
        + os.path.join(app.instance_path, "flaskr.sqlite"),
        SQLALCHEMY_TRACK_MODIFICATIONS=False,
    )  # sets default configuration for app to use, SECRET_KEY to be removed

    # To be removed if NO test are written, test_config input also
    if test_config is None:
        # load the instance config, if it exists, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # make sute isntance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)  # initialize the app with the extension

    app.register_blueprint(auth.bp)

    app.register_blueprint(home.bp)
    app.add_url_rule("/", endpoint="index")

    app.register_blueprint(plants.bp)
    app.add_url_rule("/plants", endpoint="index")

    return app
