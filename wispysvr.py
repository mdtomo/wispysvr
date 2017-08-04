from flask import Flask, request, abort, render_template, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
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
                token = {'access_token': create_access_token(user.username)}
                redirect = {'redirect': url_for('live_view')}
                return jsonify(token, redirect), 200
            else:
                return unauthorized
        else:
            return unauthorized

    
@app.route('/liveview')
@jwt_required
def live_view():
    return render_template('probes.html', user=get_jwt_identity())

 
@app.route('/wispy/<key>', methods=['POST'])
@jwt_required
def probe_receiver(key):
    print(request.json)
    return '%s' % key


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True) # pragma: no cover
    