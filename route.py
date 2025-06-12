from bottle import Bottle, run, TEMPLATE_PATH, request, response
from bottle_sqlite import SQLitePlugin
import os
import sqlite3
import uuid

from config import DATABASE, SECRET_KEY

from app.controllers.routes_setup import setup_routes
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

APP_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(os.path.join(APP_ROOT_DIR, 'views'))

app = Bottle()
app.install(SQLitePlugin(dbfile=os.path.join(APP_ROOT_DIR, DATABASE)))

sessions = {}

@app.hook('before_request')
def setup_session():
    session_id = request.get_cookie("session_id")
    if session_id and session_id in sessions:
        request.session = sessions[session_id]
    else:
        session_id = str(uuid.uuid4())
        request.session = {}
        sessions[session_id] = request.session
        response.set_cookie("session_id", session_id, path='/', httponly=True)

@app.hook('after_request')
def teardown_session():
    session_id = request.get_cookie("session_id")
    if session_id:
        sessions[session_id] = request.session

def init_db():

    os.makedirs(db_folder_path, exist_ok=True)
    db_folder_path = os.path.join(APP_ROOT_DIR, 'controllers', 'db')
    schema_path = os.path.join(db_folder_path, 'schema.sql')

    try:
        conn = sqlite3.connect(DATABASE)
        cursor = conn.cursor()

        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if not cursor.fetchone():
            with open(schema_path, 'r') as f:
                conn.executescript(f.read())
            conn.commit()
        conn.close()
    except FileNotFoundError:
        raise
    except sqlite3.OperationalError as e:
        raise


init_db()

setup_routes(app, APP_ROOT_DIR)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
