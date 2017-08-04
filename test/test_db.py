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
        hash = db.verify_password(setup.string_to_hash(setup.test_passwd), setup.test_passwd) 
        assert hash == True, 'Matching password string and hash should return True.'

    
    def test_verify_password_not_matching(self, setup):
        hash = db.verify_password(setup.string_to_hash(setup.test_passwd), 'random passwd') 
        assert hash == False, 'Unmatching password string and hash should return False.'
    


    #def test_get_user(self)