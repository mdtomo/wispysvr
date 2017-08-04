import pytest
import sys, os
sys.path.append(os.path.abspath('..'))
import db


class SetupForTest(object):

    def __init__(self):
        self.test_user = 'test'
        self.test_passwd = 'test'
        #self.test_creds = ('test', 'test')
        print('Connecting to mongodb...')
        db.connect()
        print('Creating user "test"...')
        db.create_user(username=self.test_user, password=self.test_passwd)


    def string_to_hash(self, string):
        return db.hash_password(string)


@pytest.fixture(scope='session')
def setup():
    yield SetupForTest()