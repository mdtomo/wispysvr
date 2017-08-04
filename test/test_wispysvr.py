import pytest
import sys
import os
sys.path.append(os.path.abspath('..'))
from flask import json
import wispysvr

        

class TestWispysvr(object):
    
    @pytest.fixture(scope='session')
    def flask_instance(self):
        wispysvr.app.testing = True
        app = wispysvr.app.test_client()
        return app
        
    
    @pytest.fixture(scope='session')
    def header_with_token(self):
        authenticated = self.successful_login_response()
        access_token = json.loads(authenticated.data)[0]['access_token']
        return {'Authorization':'Bearer ' + access_token}
    
    
    def successful_login_response(self):
        flask_instance = self.flask_instance()
        return flask_instance.post('/login', data=dict(username='test', password='test'), follow_redirects=True)
    

    def test_get_main_route_view(self, flask_instance):
        response = flask_instance.get('/')
        assert response.status_code == 200


    def test_get_live_view(self, flask_instance):
        response = flask_instance.get('/liveview')
        assert response.status_code == 401, 'Protected live view route should return status 401.'


    def test_get_live_view_authenticated(self, flask_instance, header_with_token):
        response = flask_instance.get('/liveview', headers=header_with_token)
        assert response.status_code == 200, 'Protected live route should return status 200 with valid authorization header.'


    def test_post_wispy_api(self, flask_instance):
        response = flask_instance.post('/wispy/1')
        assert response.status_code == 401, 'Protected wispy api post route should return status 401.'


    def test_post_login_auth_fail(self, flask_instance):
        response = flask_instance.post('/login', data=dict(username='', password=''), follow_redirects=True)
        assert response.status_code == 401, 'Lack of credentials should return status 401.'


    def test_post_login_auth_incorrect(self, flask_instance):
        response = flask_instance.post('/login', data=dict(username='wronguser', password='wrongpass'), follow_redirects=True)
        assert response.status_code == 401, 'Incorrect credentials should return status 401.'


    def test_post_login_auth_success_status(self, flask_instance, setup):
        response = flask_instance.post('/login', data=dict(username=setup.test_user, password=setup.test_passwd), follow_redirects=True)
        assert response.status_code == 200, 'Correct credentials should return status 200.'


    def test_post_login_auth_token_length(self, flask_instance, setup):
        response = flask_instance.post('/login', data=dict(username=setup.test_user, password=setup.test_passwd), follow_redirects=True)
        token_len = len(json.loads(response.data)[0]['access_token'])
        assert token_len == 297, 'Auth token length should be 297.'

