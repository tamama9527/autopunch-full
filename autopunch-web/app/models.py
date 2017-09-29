from app import db
import app
import hashlib
from flask_login import UserMixin
class user(UserMixin,db.Model):
    __tablename__ = 'user'
    id=db.Column(db.Integer, primary_key=True)
    username=db.Column(db.String(50))
    password = db.Column(db.String(120), unique=False)
    is_run=db.Column(db.Boolean)

    def __init__(self, username, password):
        self.username = username
        self.password = password
        self.is_run = True

    def __repr__(self):
        return '<User %r>' % (self.username)

    def is_authenticated(self):
        return True

    def is_active(self):   
        return True           

    def is_anonymous(self):
        return False          

    def get_user(self):         
        return str(self.username)

    def get_is_run(self):
        return self.is_run
