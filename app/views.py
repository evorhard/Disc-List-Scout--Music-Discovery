from urllib import parse as urllibparse

from datetime import datetime
from flask import Blueprint, jsonify, redirect, session, render_template, request
from loguru import logger

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
    get_user_information,
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
def user_information():
    if "access_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")

    user_information = get_user_information(session["access_token"])

    session["user_id"] = user_information.id
    session["display_name"] = user_information.display_name

    return redirect("/main")


@views_blueprint.route("/main")
def main_page():
    if "access_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")

    return render_template("index.html", username=session["display_name"])


@views_blueprint.route("/playlists")
def get_playlists():
    if "user_id" not in session:
        return redirect("/login")

    playlists = get_user_playlist(session["access_token"])

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
