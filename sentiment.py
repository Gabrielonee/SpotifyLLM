import pandas as pd
import spotipy 
from spotipy.oauth2 import SpotifyClientCredentials, SpotifyOAuth
import os
from dotenv import load_dotenv

#Env variables
load_dotenv('variables.env')

class SpotifyMoodAnalyzer:
    def __init__(self, client_id=None, client_secret=None, redirect_uri=None):
        self.client_id = client_id or os.getenv('SPOTIFY_CLIENT_ID')
        self.client_secret = client_secret or os.getenv('SPOTIFY_CLIENT_SECRET')
        self.redirect_uri = redirect_uri or os.getenv('SPOTIFY_REDIRECT_URI')
        
        self.sp = spotipy.Spotify(
            client_credentials_manager=SpotifyClientCredentials(
                client_id=self.client_id,
                client_secret=self.client_secret
            )
        )
        
    def authenticate_user(self, scope=None):
        if scope is None:
            scope = [
                'user-library-read',
                'user-top-read',
                'user-read-recently-played',
                'playlist-read-private',
                'playlist-modify-private',
                'playlist-modify-public'
            ]
        
        sp_oauth = SpotifyOAuth(
            client_id=self.client_id,
            client_secret=self.client_secret,
            redirect_uri=self.redirect_uri,
            scope=' '.join(scope)
        )
        
        # Autentica l'utente
        return spotipy.Spotify(auth_manager=sp_oauth)
    
    def get_user_data(self, sp_user):
        user_profile = sp_user.current_user()
        
        top_tracks_medium = sp_user.current_user_top_tracks(time_range='medium_term', limit=10)
        top_artists_medium = sp_user.current_user_top_artists(time_range='medium_term', limit=10)
        
        recently_played = sp_user.current_user_recently_played(limit=10)
        
        genres = []
        for artist in top_artists_medium['items']:
            genres.extend(artist['genres'])
        genre_counts = pd.Series(genres).value_counts().to_dict()
        
        return {
            'user_profile': user_profile,
            'top_tracks': top_tracks_medium,
            'top_artists': top_artists_medium,
            'recently_played': recently_played,
            'top_genres': genre_counts
        }
