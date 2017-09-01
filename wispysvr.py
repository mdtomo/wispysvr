from flask import Flask, request, abort, render_template, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity, jwt_refresh_token_required, create_refresh_token
from mongoengine import errors
import db

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')
jwt = JWTManager(app)
db.connect()


@app.route('/')
def login_view():
    #db.create_user(username='test', password='test')
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_process():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        unauthorized = ('Bad username or password.', 401)
        if db.check_user_exists(username):
            if db.check_user_password(username, password):
                user = db.get_user(username)
                tokens = {'access_token': create_access_token(identity=user.username),
                          'refresh_token': create_refresh_token(identity=user.username)}
                redirect = {'redirect': url_for('live_view')}
                print(tokens)
                return jsonify(tokens, redirect), 200
            else:
                return unauthorized
        else:
            return unauthorized

    
@app.route('/liveview')
@jwt_required
def live_view():
    return render_template('probes.html', user=get_jwt_identity())

 
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
    app.run(host='0.0.0.0', debug=True) # pragma: no cover
    