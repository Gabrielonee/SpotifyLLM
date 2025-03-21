from flask import Flask, request, redirect, render_template
from sentiment import SpotifyMoodAnalyzer
import os
app = Flask(__name__)


client_id = os.getenv('SPOTIFY_CLIENT_ID')
client_secret = os.getenv('SPOTIFY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIFY_REDIRECT_URI')


mood_analyzer = SpotifyMoodAnalyzer(client_id, client_secret, redirect_uri)

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/user_recap')
def user_recap():
    sp_user = mood_analyzer.authenticate_user()
    user_data = mood_analyzer.get_user_data(sp_user)

    print(user_data)  # Stampa tutta la struttura per vedere cosa è presente

    return render_template('user_recap.html',
                           user=user_data['user_profile']['display_name'],
                           top_tracks = [
                            {
                                'name': track['name'],
                                'artist': track['artists'][0]['name'],  # Primo artista
                                'album': track['album']['name'],
                                'image_url': track['album']['images'][0]['url'] if track['album']['images'] else None
                            } for track in user_data.get('top_tracks', {}).get('short_term', {}).get('items', [])
                            ],
                            top_artists=[artist['name'] for artist in user_data.get('top_artists', {}).get('short_term', {}).get('items', [])[:5]],
                            top_genres=list(user_data.get('top_genres', {}).keys())[:5],
                            recently_played=[{
                               'name': track['track']['name'],
                               'artist': track['track']['artists'][0]['name'],
                               'image': track['track']['album']['images'][0]['url'],
                               'url': track['track']['external_urls']['spotify']
                           } for track in user_data.get('recently_played', {}).get('items', [])[:5]]
                           )
if __name__ == '__main__':
    app.run(debug=True, port=5001)