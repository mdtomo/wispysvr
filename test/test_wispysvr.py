import sys
import os
sys.path.append(os.path.abspath('..'))
import wispysvr
import unittest
from flask import json

class WispysvrTestCase(unittest.TestCase):

	username = 'test'
	password = 'test'

	def setUp(self):
		wispysvr.app.testing = True
		self.app = wispysvr.app.test_client()


	def login(self, username, password):
		return self.app.post('/login', data=dict(username=username, password=password), follow_redirects=True)


	def header_with_token(self):
		authenticated = self.login(self.username, self.password)
		access_token = json.loads(authenticated.data)[0]['access_token']
		return {'Authorization':'Bearer ' + access_token}


	def test_get_main_route_view(self):
		response = self.app.get('/')
		self.assertEqual(response.status_code, 200, 'Unprotected main route should return status 200.')


	def test_get_live_view(self):
		response = self.app.get('/liveview')
		self.assertEqual(response.status_code, 401, 'Protected live view route should return status 401.')


	def test_get_live_view_authenticated(self):
		response = self.app.get('/liveview', headers=self.header_with_token())
		self.assertEqual(response.status_code, 200, 'Protected live route should return status 200 with valid authorization header.')


	def test_post_wispy_api(self):
		response = self.app.post('/wispy/1')
		self.assertEqual(response.status_code, 401, 'Protected wispy api post route should return status 401.')


	def test_post_login_auth_fail(self):
		response = self.login('','')
		self.assertEqual(response.status_code, 401, 'Lack of credentials should return status 401.')


	def test_post_login_auth_incorrect(self):
		response = self.login('wronguser','wrongpass')
		self.assertEqual(response.status_code, 401, 'Lack of credentials should return status 401.')


	def test_post_login_auth_success_status(self):
		response = self.login(self.username, self.password)
		self.assertEqual(response.status_code, 200, 'Correct credentials should return status 200.')


	def test_post_login_auth_token_length(self):
		response = self.login(self.username, self.password)
		token_length = len(json.loads(response.data)[0]['access_token'])
		self.assertEqual(token_length, 297, 'Auth token length should be 297.')



if __name__ == '__main__':
    unittest.main()