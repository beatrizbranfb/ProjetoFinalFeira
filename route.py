from bottle import Bottle, run, TEMPLATE_PATH, request, response
import os
import uuid

from app.controllers.routes_setup import RouteRenderer
import sys

sys.path.insert(0, os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app'))

APP_ROOT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'app')
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
TEMPLATE_PATH.append(os.path.join(APP_ROOT_DIR, 'views'))

app = Bottle()
route_render = RouteRenderer()

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

route_render.setup_routes(app, APP_ROOT_DIR)

if __name__ == '__main__':
    run(app, host='localhost', port=8080, debug=True)
