from urllib import parse as urllibparse

from flask import Blueprint, jsonify, redirect, session, request
from datetime import datetime

# Local imports
from config import (
    API_BASE_URL,
    AUTHORIZATION_URL,
    CLIENT_ID,
    CLIENT_SECRET,
    REDIRECT_URI,
    SCOPE,
    TOKEN_URL,
)
from spotify_authorization import (
    exchange_code_for_token,
    get_user_id,
    get_user_playlist,
    refresh_token,
)

views_blueprint = Blueprint("views", __name__)


@views_blueprint.route("/")
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"


@views_blueprint.route("/login")
def login():
    """Initial login screen

    Returns:
        redirect -- Redirects to authorization screen
    """
    login_url_parameters = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": SCOPE,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": True,
    }

    authorization_url = (
        f"{AUTHORIZATION_URL}?{urllibparse.urlencode(login_url_parameters)}"
    )

    return redirect(authorization_url)


@views_blueprint.route("/callback")
def callback():
    """Callback

    Returns:
        redirect -- Redirects to getting the user id page
    """
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})

    if "code" in request.args:
        token_info = exchange_code_for_token(
            request.args["code"], CLIENT_ID, CLIENT_SECRET, REDIRECT_URI, TOKEN_URL
        )

        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]

        return redirect("/user-id")


@views_blueprint.route("/user-id")
def user_id():
    if "access_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")

    session["user_id"] = get_user_id(session["access_token"], API_BASE_URL)

    return redirect("/playlists")


@views_blueprint.route("/playlists")
def get_playlists():
    if "user_id" not in session:
        return redirect("/login")

    playlists = get_user_playlist(
        session["access_token"], API_BASE_URL, session["user_id"]
    )

    return jsonify(playlists)


@views_blueprint.route("/refresh-token")
def refresh_token():
    if "refresh_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]:
        new_token_info = refresh_token(
            session["refresh_token"], CLIENT_ID, CLIENT_SECRET, TOKEN_URL
        )

        session["access_token"] = new_token_info["access_token"]
        session["expires_at"] = (
            datetime.now().timestamp() + new_token_info["expires_in"]
        )

    return redirect("/playlists")
