import sqlite3

import click
from flask import current_app, g
from flask.cli import with_appcontext

# g is a special object that's unique for each request, it's used to store data that might be accessed by multiple functions during the request, the connection is stored and reused instead of creating a new connection if get_db is called a second time in the same request

# current_app is a special object that points to the Flask application that is handing the request, since I'm using an application factory there is no application object when writing the rest of my code. get_db will be called when the application has been created and is handling the request so current_app can be used

# sqlite3.connect() establishes the connection to the file pointed at by DATABASE configuration key
# sqlite3.Row tells the connection established by sqlite3.connect() to return rows that behave like dicts, this allows accessing the columns by name

def get_db():
    if 'db' not in g:
        g.db = sqlite3.connect(
            current_app.config['DATABASE'],
            detect_types=sqlite3.PARSE_DECLTYPES
        )
        g.db.row_factory = sqlite3.Row

    return g.db

# close_db() checks if a connection was created by checking if g.db was set, if the connection exists it is closed 
def close_db(e=None):
    db = g.pop('db', None)

    if db is not None:
        db.close()
