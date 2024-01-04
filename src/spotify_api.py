import config
import spotipy

from spotipy.oauth2 import SpotifyOAuth


def spotify_authenticate():
    authentication_manager = SpotifyOAuth(
        client_id=config.SPOTIFY_CLIENT_ID,
        client_secret=config.SPOTIFY_CLIENT_SECRET,
        redirect_uri=config.SPOTIFY_REDIRECT_URI,
        scope="playlist-modify-public",
    )

    spotify = spotipy.Spotify(auth_manager=authentication_manager)

    return spotify


def create_playlist(spotify, name, description):
    user_id = spotify.current_user()["id"]
    playlist = spotify.user_playlist_create(user_id, name, description=description)

    return playlist
