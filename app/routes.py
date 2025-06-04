from flask import render_template, redirect, url_for, request, flash
from flask_login import login_user, logout_user, login_required, current_user
from datetime import datetime
from . import app, db
from .models import User, Team, Reservation, Match

@app.route('/')
def index():
    reservations = Reservation.query.order_by(Reservation.start_time).all()
    return render_template('index.html', reservations=reservations)

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        email = request.form['email']
        password = request.form['password']
        if User.query.filter_by(username=username).first():
            flash('Username already taken')
            return redirect(url_for('register'))
        user = User(username=username, email=email, password=password)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        return redirect(url_for('profile'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('profile'))
        flash('Invalid credentials')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/profile')
@login_required
def profile():
    return render_template('profile.html')

@app.route('/reservation', methods=['POST'])
@login_required
def make_reservation():
    start = datetime.fromisoformat(request.form['start'])
    end = datetime.fromisoformat(request.form['end'])
    r = Reservation(user_id=current_user.id, start_time=start, end_time=end, paid=False)
    db.session.add(r)
    db.session.commit()
    flash('Reservation made! Please pay at the counter.')
    return redirect(url_for('index'))

@app.route('/team/create', methods=['POST'])
@login_required
def create_team():
    name = request.form['name']
    if Team.query.filter_by(name=name).first():
        flash('Team name already exists')
        return redirect(url_for('profile'))
    team = Team(name=name)
    db.session.add(team)
    db.session.commit()
    current_user.team = team
    db.session.commit()
    flash('Team created')
    return redirect(url_for('profile'))

@app.route('/leaderboard')
def leaderboard():
    teams = Team.query.order_by(Team.wins.desc()).all()
    return render_template('leaderboard.html', teams=teams)
