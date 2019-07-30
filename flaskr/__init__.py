import os

from flask import Flask

# create_app is the application factory function
def create_app(test_config=None):
    # create and configure the app
    app = Flask(__name__, instance_relative_config=True) # creates the Flask instance; __name__ is the name of the current Python module; instance_relative_config=True tells the app that configuration files are relative to the instance folder

    # app.config.from_mapping() sets default configuration that the app will use
    app.config.from_mapping(
        SECRET_KEY='dev', # it's used by Flask and extensions to keep the data safe, it should be overriden by random value when deploying
        DATABASE=os.path.join(app.instance_path, 'flaskr.sqlite'), # path to SQLite database file
    )

    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True) # app.config.from_pyfile() overrides the default configuration with the values taken from config.py file in the instance folder if it exists
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config) # test_config can also be passed to the factory, and used instead of the instance configuration; this is for the tests I write can be configured independently of any development values I have configured

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path) # the os.makedirs makes sure that the app.instance_path exists, flask will not create an instance folder automatically but it needs to be created because this project will create the SQLite database folder there
    except OSError:
        pass


    # a simple page that says hello
    # app.route creates a simple route to see the application in working -- it creates a connection between the URL /hello and the function that returns "Hello, World!"
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app
