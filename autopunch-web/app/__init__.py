from flask import Flask, url_for,render_template,flash,redirect
import flask_login
from form import LoginForm
from flask_sqlalchemy import SQLAlchemy
from fileconfig import *
app = Flask(__name__)
#flask config
app.config.from_object('fileconfig')
#database setting
db = SQLAlchemy(app)
db.create_all()
#login manager
login_manager = flask_login.LoginManager()
login_manager.init_app(app)
from app import views
