from flask import Flask
import os
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

frontend_build = os.path.join(os.path.dirname(__file__), '..', 'frontend', 'dist')
app = Flask(__name__, static_folder=frontend_build, static_url_path='/')
app.config['SECRET_KEY'] = 'change_this_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///football.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)

from . import routes, models
