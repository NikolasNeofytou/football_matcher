from flask import jsonify, request, send_from_directory
from flask_login import login_user, logout_user, login_required, current_user
import os
from datetime import datetime, timedelta, time
from . import app, db
from .models import User, Team, Reservation, Match

@app.route('/api/schedule')
def api_schedule():
    start_date = datetime.now().date()
    hours = list(range(8, 22))
    schedule = []
    for day in range(7):
        date = start_date + timedelta(days=day)
        slots = []
        for hr in hours:
            slot_start = datetime.combine(date, time(hr, 0))
            slot_end = slot_start + timedelta(hours=1)
            reserved = Reservation.query.filter(
                Reservation.start_time <= slot_start,
                Reservation.end_time > slot_start
            ).first()
            slots.append({
                'start': slot_start.isoformat(),
                'end': slot_end.isoformat(),
                'reserved': reserved is not None
            })
        schedule.append({'date': date.isoformat(), 'slots': slots})
    return jsonify({'hours': hours, 'schedule': schedule})

@app.route('/api/register', methods=['POST'])
def api_register():
    data = request.get_json()
    username = data.get('username')
    email = data.get('email')
    password = data.get('password')
    if User.query.filter_by(username=username).first():
        return jsonify({'error': 'Username taken'}), 400
    user = User(username=username, email=email, password=password)
    db.session.add(user)
    db.session.commit()
    login_user(user)
    return jsonify({'message': 'registered'})

@app.route('/api/login', methods=['POST'])
def api_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    user = User.query.filter_by(username=username, password=password).first()
    if user:
        login_user(user)
        return jsonify({'message': 'logged in'})
    return jsonify({'error': 'Invalid credentials'}), 401

@app.route('/api/logout')
@login_required
def api_logout():
    logout_user()
    return jsonify({'message': 'logged out'})

@app.route('/api/profile')
@login_required
def api_profile():
    team = None
    if current_user.team:
        team = {
            'id': current_user.team.id,
            'name': current_user.team.name,
            'wins': current_user.team.wins,
            'losses': current_user.team.losses
        }
    return jsonify({
        'id': current_user.id,
        'username': current_user.username,
        'email': current_user.email,
        'team': team
    })

@app.route('/api/reservation', methods=['POST'])
@login_required
def api_make_reservation():
    data = request.get_json()
    start = datetime.fromisoformat(data['start'])
    end = datetime.fromisoformat(data['end'])
    r = Reservation(user_id=current_user.id, start_time=start, end_time=end, paid=False)
    db.session.add(r)
    db.session.commit()
    return jsonify({'message': 'Reservation made'})

@app.route('/api/team/create', methods=['POST'])
@login_required
def api_create_team():
    data = request.get_json()
    name = data.get('name')
    if Team.query.filter_by(name=name).first():
        return jsonify({'error': 'Team exists'}), 400
    team = Team(name=name)
    db.session.add(team)
    db.session.commit()
    current_user.team = team
    db.session.commit()
    return jsonify({'message': 'team created'})

@app.route('/api/leaderboard')
def api_leaderboard():
    teams = Team.query.order_by(Team.wins.desc()).all()
    output = []
    for t in teams:
        output.append({'id': t.id, 'name': t.name, 'wins': t.wins, 'losses': t.losses})
    return jsonify({'teams': output})

@app.route('/', defaults={'path': ''})
@app.route('/<path:path>')
def serve_react(path):
    """Serve the compiled React app or show a helpful message if missing."""
    if os.path.exists(app.static_folder):
        if path != '' and os.path.exists(os.path.join(app.static_folder, path)):
            return send_from_directory(app.static_folder, path)
        index_path = os.path.join(app.static_folder, 'index.html')
        if os.path.exists(index_path):
            return send_from_directory(app.static_folder, 'index.html')
    return (
        "Frontend build not found. Run 'npm run build' inside the frontend folder.",
        404,
    )
