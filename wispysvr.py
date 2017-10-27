from flask import Flask, request, abort, render_template, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, jwt_refresh_token_required, create_refresh_token, set_access_cookies, set_refresh_cookies, unset_jwt_cookies
from flask_socketio import SocketIO, Namespace, emit, join_room, leave_room
from flask_cors import CORS, cross_origin
from mongoengine import errors
import db
import functools
import logging

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')
jwt = JWTManager(app)
CORS(app, origins='http://localhost:8081', supports_credentials=True)
socketio = SocketIO(app, engineio_logger=True)
db.connect()


def authentication_required(f):
    """
    Custom decorator function to check if the user is authenticated before allowing
    socketio connections.
    """
    @functools.wraps(f)
    def wrapped(*args, **kwargs):
        print('authentication_required called ', args, kwargs)
    return wrapped


@socketio.on('connect', namespace='/')
# @authentication_required
def socket_connection():
    print('Clients connected', socketio.server.manager.rooms['/'])
    print('Socket io client cookies ', request.cookies)
    emit('wispysvr', 'You are connected')


@socketio.on('disconnect', namespace='/')
def socket_disconnection():
    print('Client disconnected', socketio.server.manager.rooms['/'])


@socketio.on('authorization')
def on_authorization(json):
    # print(json['data'])
    join_room(json['data']['user'])
    print('Clients connected room', socketio.server.manager.rooms['/'])
    print('Socket io auth test req headers: ', request.cookies)


@socketio.on('log out')
def on_log_out(data):
    print(data['data'])
    leave_room(data['data'])


@socketio.on('wispysvr-frontend', namespace='/')
def socket_message(message):
    print('wispy-frontend: ', message)


@app.route('/')
def login_view():
    #db.create_user(username='test', password='test')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        unauthorized = ('Bad username or password.', 401)
        if db.check_user_exists(username):
            ''' User exists '''
            if db.check_user_password(username, password):
                ''' Password matches hash '''
                user = db.get_user(username)
                authorized = jsonify({ 'authorized': True })
                access_token = create_access_token(identity=user.username)
                refresh_token = create_refresh_token(identity=user.username)
                set_access_cookies(authorized, access_token)
                set_refresh_cookies(authorized, refresh_token)
                return authorized
            else:
                return unauthorized
        else:
            return unauthorized


@app.route('/logout')
def logout():
    response = jsonify({ 'authorized': False })
    unset_jwt_cookies(response)
    return (response, 200)

 
@app.route('/wispy', methods=['POST'])
@jwt_required
def probe_receiver():
    print(request.get_json())
    db.create_probe(get_jwt_identity(), request.get_json())
    return ('OK', 200)


@app.route('/probes')
@jwt_required
def probes():
    return (db.get_probes_by_time(), 200)


@app.route('/refresh', methods=['POST'])
@jwt_refresh_token_required
def refresh():
    user = get_jwt_identity()
    token = {'access_token': create_access_token(identity=user)}
    return (jsonify(token), 200)


if __name__ == '__main__':
    # app.run(host='0.0.0.0', debug=True) # pragma: no cover
    socketio.run(app, host='0.0.0.0') # pragma: no cover
    