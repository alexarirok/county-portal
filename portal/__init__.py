import os
from flask import Flask

def create_app(test_config=None):
    app = Flask(__name__, instance_relative_config=True)
    app.config.from_mapping(
        SECRET_KEY = "DEVELOPMENT",
        DATABASE=os.path.join(app.instance_path, "portal.sqlite3"),
    )
    if test_config is None:
        #load instance config if it exist, when not testing
        app.config.from_pyfile("config.py", silent=True)
    else:
        # load test config if passed in
        app.config.from_mapping(test_config)

    #ensure instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    #simple page that say hello you
    @app.route('/hello')
    def hello():
        return "Hello you!"
    return app
    def create_app():
        app = ...
    # existing code omitted
        from . import db
        db.init_app(app)

        from . import auth
        app.register_blueprint(auth.pd)

        return app