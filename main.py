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
    """Recupera e stampa un recap dell'utente"""
    try:
        sp_user = mood_analyzer.authenticate_user()
        user_data = mood_analyzer.get_user_data(sp_user)

        user_profile = user_data['user_profile']
        top_genres = user_data['top_genres']
        top_tracks = [track['name'] for track in user_data['top_tracks']['items']]
        top_artists = [artist['name'] for artist in user_data['top_artists']['items']]
        recently_played = [track['track']['name'] for track in user_data['recently_played']['items']]


        print(f"Utente: {user_profile['display_name']}")
        print(f"ID: {user_profile['id']}")
        print(f"Generi preferiti: {list(top_genres.keys())[:5]}")
        print(f"Top brani: {top_tracks[:5]}")
        print(f"Top artisti: {top_artists[:5]}")
        print(f"Ultimi ascolti: {recently_played[:5]}")

        return {
            "user": user_profile['display_name'],
            "top_genres": list(top_genres.keys())[:5],
            "top_tracks": top_tracks[:5],
            "top_artists": top_artists[:5],
            "recently_played": recently_played[:5]
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == '__main__':
    app.run(debug=True, port=5001)