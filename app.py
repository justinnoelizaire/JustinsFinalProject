from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from werkzeug.security import generate_password_hash, check_password_hash
import os

# Get the absolute path to the directory containing app.py
BASE_DIR = os.path.abspath(os.path.dirname(__file__))

app = Flask(__name__,
           template_folder=os.path.join(BASE_DIR, 'templates'),
           static_folder=os.path.join(BASE_DIR, 'static'))

app.config['SECRET_KEY'] = 'your-secret-key'  # Change this in production
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{os.path.join(BASE_DIR, "basketball.db")}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Models
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password_hash = db.Column(db.String(120), nullable=False)
    favorite_team = db.Column(db.String(80))

class Team(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    players = db.relationship('Player', backref='team', lazy=True)

class Player(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    team_id = db.Column(db.Integer, db.ForeignKey('team.id'), nullable=False)
    position = db.Column(db.String(10))
    points_per_game = db.Column(db.Float, default=0.0)
    rebounds_per_game = db.Column(db.Float, default=0.0)
    assists_per_game = db.Column(db.Float, default=0.0)
    steals_per_game = db.Column(db.Float, default=0.0)
    blocks_per_game = db.Column(db.Float, default=0.0)
    field_goal_percentage = db.Column(db.Float, default=0.0)
    three_point_percentage = db.Column(db.Float, default=0.0)

class Game(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    home_team = db.Column(db.String(80), nullable=False)
    away_team = db.Column(db.String(80), nullable=False)
    date = db.Column(db.DateTime, nullable=False)
    score_home = db.Column(db.Integer)
    score_away = db.Column(db.Integer)

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# Routes
@app.route('/')
def home():
    app.logger.info('Accessing home page')
    return render_template('home.html')

@app.route('/stats')
def stats():
    app.logger.info('Accessing stats page')
    players = Player.query.order_by(Player.points_per_game.desc()).all()
    return render_template('stats.html', players=players)

@app.route('/rankings')
def rankings():
    app.logger.info('Accessing rankings page')
    teams = Team.query.order_by(Team.wins.desc()).all()
    return render_template('rankings.html', teams=teams)

@app.route('/schedule')
def schedule():
    app.logger.info('Accessing schedule page')
    games = Game.query.all()
    return render_template('schedule.html', games=games)

@app.route('/profile')
@login_required
def profile():
    app.logger.info('Accessing profile page')
    return render_template('profile.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        user = User.query.filter_by(username=request.form['username']).first()
        if user and check_password_hash(user.password_hash, request.form['password']):
            login_user(user)
            return redirect(url_for('home'))
        flash('Invalid username or password')
    app.logger.info('Accessing login page')
    return render_template('login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        hashed_password = generate_password_hash(request.form['password'])
        user = User(username=request.form['username'], 
                   password_hash=hashed_password,
                   favorite_team=request.form.get('favorite_team'))
        db.session.add(user)
        db.session.commit()
        return redirect(url_for('login'))
    app.logger.info('Accessing register page')
    return render_template('register.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    app.logger.info('Logging out')
    return redirect(url_for('home'))

if __name__ == '__main__':
    print(f"Template folder: {app.template_folder}")
    print(f"Static folder: {app.static_folder}")
    with app.app_context():
        db.create_all()
    app.run(debug=True, port=5004)
