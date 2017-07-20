from flask import Flask, request, abort, render_template, jsonify, redirect, url_for
from flask_jwt_extended import JWTManager, jwt_required, create_access_token, get_jwt_identity
import db

app = Flask(__name__)
app.config.from_envvar('APP_CONFIG')
jwt = JWTManager(app)
db = db.MongoEngine(app)

@app.route('/')
def login_view():
    return render_template('login.html')


@app.route('/login', methods=['POST'])
def login_process():
    if request.method == 'POST':
        if check_credentials(request.form):
            token = {'access_token': create_access_token(request.form['username'])}
            redirect = {'redirect': url_for('live_view')}
            return jsonify(token, redirect), 200
        else:
            return 'Bad username or password.', 401

    
@app.route('/liveview')
@jwt_required
def live_view():
    return render_template('probes.html', user=get_jwt_identity())

 
@app.route('/wispy/<key>', methods=['POST'])
@jwt_required
def probe_receiver(key):
    print(request.json)
    return '%s' % key


def check_credentials(credentials):
    if credentials['username'] == 'test' and credentials['password'] == 'test':
        return True
    else:
        return False


if __name__ == '__main__':
    app.run() # pragma: no cover
    