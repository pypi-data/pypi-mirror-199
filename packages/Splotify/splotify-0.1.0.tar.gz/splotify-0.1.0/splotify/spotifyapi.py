import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth


class SpotifyApi:
    def __init__(self, client_id, client_secret, redirect_uri):
        os.environ["SPOTIPY_CLIENT_ID"] = client_id
        os.environ["SPOTIPY_CLIENT_SECRET"] = client_secret
        os.environ["SPOTIPY_REDIRECT_URI"] = redirect_uri

        scope = """playlist-read-collaborative
            playlist-read-private
            playlist-modify-private
            playlist-modify-public
            user-follow-read
            user-follow-modify
            user-library-modify
            user-library-read
            user-modify-playback-state
            user-read-currently-playing
            user-read-playback-state
            user-read-playback-position
            user-read-private
            user-read-recently-played"""

        self.sp = spotipy.Spotify(auth_manager=SpotifyOAuth(scope=scope))

    def search(self, query, limit, type):
        return self.sp.search(q=query, limit=limit, type=type)

    def current_user_playlists(self):
        return self.sp.current_user_playlists()

    def track(self, id):
        return self.sp.track(id)

    def album(self, id):
        return self.sp.album(id)

    def playlist(self, id):
        return self.sp.playlist(id)

    def audio_features(self, id):
        return self.sp.audio_features(id)
