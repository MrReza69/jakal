
from flask import Flask, render_template, request
import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import os

app = Flask(__name__)

# Spotify API
client_id = os.getenv('fcb2ecd28fba41e8ad40f986532ffd96', 'b07fb0c02a0e4ef7b60529e39e3d6c09')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET', 'your_spotify_client_secret')
sp = spotipy.Spotify(auth_manager=SpotifyClientCredentials(client_id=client_id, client_secret=client_secret))

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/search', methods=['POST'])
def search():
    query = request.form['query']
    results = sp.search(q=query, type='track', limit=10)
    tracks = results['tracks']['items']
    return render_template('results.html', tracks=tracks)

@app.route('/play/<track_id>')
def play(track_id):
    track = sp.track(track_id)
    return render_template('play.html', track=track)

if __name__ == '__main__':
    app.run(debug=True)






