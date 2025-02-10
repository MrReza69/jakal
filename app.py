from flask import Flask, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user, current_user
from flask_sqlalchemy import SQLAlchemy
from models import db, User, Search
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize extensions
db.init_app(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'

# Spotify API
client_id = os.getenv('SPOTIPY_CLIENT_ID', 'fcb2ecd28fba41e8ad40f986532ffd96')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET', 'b07fb0c02a0e4ef7b60529e39e3d6c09')
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User(username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Registration successful! Please log in.', 'success')
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username, password=password).first()
        if user:
            login_user(user)
            return redirect(url_for('index'))
        else:
            flash('Login failed. Check your username and password.', 'danger')
    return render_template('login.html')

@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/search', methods=['POST'])
@login_required
def search():
    query = request.form['query']
    results = sp.search(q=query, type='track', limit=10)
    tracks = results['tracks']['items']
    
    # Save search to database
    search = Search(query=query, user_id=current_user.id)
    db.session.add(search)
    db.session.commit()
    
    return render_template('results.html', tracks=tracks)

@app.route('/play/<track_id>')
@login_required
def play(track_id):
    track = sp.track(track_id)
    return render_template('play.html', track=track)

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)