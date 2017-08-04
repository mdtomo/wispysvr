
''' Handle all interactions with Mongodb from db.py'''

import mongoengine as db
import datetime
import time
import os
import nacl.pwhash


def connect():
    try:
        db.connect('wispysvr', host='wispysvrdb', port=27017)
        print(os.getenv('APP_CONFIG'))
        time.sleep(1)
    except db.MongoEngineConnectionError as e:
        print(e)
       

class LogUser(db.EmbeddedDocument):
    ts = db.DateTimeField(default=datetime.datetime.utcnow())
    ip = db.StringField(max_length=15)


class MacAlias(db.EmbeddedDocument):
    mac = db.StringField(max_length=17, min_length=17)
    alias = db.StringField(max_length=50)

    
class User(db.Document):
    username = db.StringField(max_length=50, min_length=4, required=True, unique=True)
    email = db.EmailField(unique=True)
    password = db.StringField(max_length=256, required=True)
    previous_logins = db.ListField(db.EmbeddedDocumentField(LogUser))
    previous_failed_logins = db.ListField(db.EmbeddedDocumentField(LogUser))
    failed_login_attempts = db.IntField(default=0)
    isAdmin = db.BooleanField(default=False)
    mac_aliases = db.ListField(db.EmbeddedDocumentField(MacAlias))
    meta = {
        'indexes': [
            'username',
            '$username' 
        ]
    }
    

def check_user_exists(username):
    try:
        user = User.objects(username=username).get()
        return True
    except db.DoesNotExist as e:
        print(e)
        return False
        
        
def check_user_password(username, passwd):
    user = User.objects(username=username).first()
    if user != None:
        print(user)
        return verify_password(user.password, passwd)
    else:
        return False


def verify_password(password_hash, passwd):
    hashed = password_hash
    if type(hashed) is str:
        hashed = hashed.encode('utf-8')    
    try:
        nacl.pwhash.verify_scryptsalsa208sha256(hashed, passwd.encode('utf-8'))
        return True
    except nacl.exceptions.InvalidkeyError as e:
        print(e)
        return False
    except nacl.exceptions.ValueError as e:
        print(e)
        return False


def hash_password(passwd):
    return nacl.pwhash.scryptsalsa208sha256_str(passwd.encode('utf-8'))


def get_user(username):
    return User.objects(username=username).first()
        

def create_user(username, password):
    try:
        user = User(username=username, password=hash_password(password))
        user.isAdmin = True
        user.save()
    except db.errors.NotUniqueError as e:
        print(e)

        
class Probe(db.Document):
    owner = db.ReferenceField(User, reverse_delete_rule=db.CASCADE)
    ts = db.ComplexDateTimeField(required=True)
    mac = db.StringField(max_length=17, min_length=17, required=True)
    channel = db.StringField(required=True)
    rssi = db.IntField(required=True)
    ssid = db.StringField(max_length=32, required=True)
    meta = {
        'indexes': [
            'ts',
            '#ts',
            'mac',
            '$mac'
        ],
        'ordering': [
            '-ts']
    }

    
def create_probe(user, request):
    Probe(owner=user, ts=request.ts, mac=request.mac, channel=request.channel, rssi=request.rssi, ssid=request.ssid).save()

