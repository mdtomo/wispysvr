import pytest
import sys
import os
sys.path.append(os.path.abspath('..'))
import db

class TestDb(object):
      
    
    def test_check_user_exists_known_user(self, setup):
        result = db.check_user_exists(setup.test_user)
        assert result == True
    
    
    def test_check_user_exists_unknown_user(self):
        result = db.check_user_exists('random user')
        assert result == False, 'Unknown user should return False.'
    
    
    def test_check_user_password_known_user(self, setup):
        result = db.check_user_password(setup.test_user, setup.test_passwd)
        assert result == True


    def test_check_user_password_unknown_user(self, setup):
        result = db.check_user_password('random', setup.test_passwd)
        assert result == False


    def test_verify_password_matching(self, setup):
        result = db.verify_password(setup.string_to_hash(setup.test_passwd), setup.test_passwd) 
        assert result == True, 'Matching password string and hash should return True.'

    
    def test_verify_password_not_matching(self, setup):
        result = db.verify_password(setup.string_to_hash(setup.test_passwd), 'random passwd') 
        assert result == False, 'Unmatching password string and hash should return False.'
    
    
    def test_verify_password_invalid_value(self, setup):
        result = db.verify_password('invalid hash', setup.test_passwd)
        assert result == False, 'Invalid hash should return False.'


    def test_hash_password(self, setup):
        hash = db.hash_password(setup.test_passwd)
        result = db.verify_password(hash, setup.test_passwd)
        assert result == True, 'Matching plain password and hash should match and return True.'


    def test_hash_password_mismatch(self, setup):
        hash = db.hash_password(setup.test_passwd)
        result = db.verify_password(hash, 'unmatching pass')
        assert result == False, 'Unmatching plain password and hash should match and return False'

    
    def test_get_user_known_user(self, setup):
        user = db.get_user(setup.test_user)
        assert user.username == setup.test_user


    def test_get_user_unknown_user(self):
        user = db.get_user('unknownuser')
        print(user)
        assert user == None


    def test_create_user_unique(self):
        result = db.create_user(username='test2', password='test')
        assert result == True


    def test_remove_user_known(self, setup):
        user = db.remove_user(username='test2')
        assert user == True




