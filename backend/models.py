from . import db, login_manager
from flask_login import UserMixin
from datetime import datetime

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), unique=True, nullable=False)
    users = db.relationship('User', backref='team', lazy=True)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)

class Reservation(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    start_time = db.Column(db.DateTime, nullable=False)
    end_time = db.Column(db.DateTime, nullable=False)
    paid = db.Column(db.Boolean, default=False)

class Match(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    team_a_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    team_b_id = db.Column(db.Integer, db.ForeignKey('team.id'))
    time = db.Column(db.DateTime, default=datetime.utcnow)
    score_a = db.Column(db.Integer)
    score_b = db.Column(db.Integer)
