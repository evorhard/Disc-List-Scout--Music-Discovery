import os
import requests

import urllib.parse

from datetime import datetime
from dotenv import load_dotenv
from flask import Flask, redirect, request, jsonify, session
from loguru import logger

load_dotenv()

app = Flask(__name__)
app.secret_key = "2d63a7aa2727ec8f939923cf3304d0d7a9e334463918395739e713b7d5dee933"

CLIENT_ID = os.environ.get("CLIENT_ID")
CLIENT_SECRET = os.environ.get("CLIENT_SECRET")
REDIRECT_URI = os.environ.get("REDIRECT_URI")

AUTHORIZATION_URL = os.environ.get("AUTHORIZATION_URL")
TOKEN_URL = os.environ.get("TOKEN_URL")
API_BASE_URL = os.environ.get("API_BASE_URL")


@app.route("/")
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"


@app.route("/login")
def login():
    scope = "user-read-private user-read-email"

    parameters = {
        "client_id": CLIENT_ID,
        "response_type": "code",
        "scope": scope,
        "redirect_uri": REDIRECT_URI,
        "show_dialog": True,
    }

    authorization_url = f"{AUTHORIZATION_URL}?{urllib.parse.urlencode(parameters)}"

    return redirect(authorization_url)


@app.route("/callback")
def callback():
    if "error" in request.args:
        return jsonify({"error": request.args["error"]})

    if "code" in request.args:
        request_body = {
            "code": request.args["code"],
            "grant_type": "authorization_code",
            "redirect_uri": REDIRECT_URI,
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        response = requests.request("POST", TOKEN_URL, data=request_body)
        token_info = response.json()

        session["access_token"] = token_info["access_token"]
        session["refresh_token"] = token_info["refresh_token"]
        session["expires_at"] = datetime.now().timestamp() + token_info["expires_in"]

        return redirect("/user-id")


@app.route("/user-id")
def get_user_id():
    if "access_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]:
        return redirect("/refresh-token")

    headers = {"Authorization": f"Bearer {session['access_token']}"}

    response = requests.request("GET", f"{API_BASE_URL}/me", headers=headers)
    user_info = response.json()

    session["user_id"] = user_info["id"]

    return redirect("/playlists")


@app.route("/playlists")
def get_playlists():
    if "user_id" not in session:
        return redirect("/login")

    headers = {"Authorization": f"Bearer {session['access_token']}"}

    response = requests.request(
        "GET", f"{API_BASE_URL}/users/{session['user_id']}/playlists", headers=headers
    )
    playlists = response.json()

    return jsonify(playlists)


@app.route("/refresh-token")
def refresh_token():
    if "refresh_token" not in session:
        return redirect("/login")

    if datetime.now().timestamp() > session["expires_at"]:
        request_body = {
            "grant_type": "refresh_token",
            "refresh_token": session["refresh_token"],
            "client_id": CLIENT_ID,
            "client_secret": CLIENT_SECRET,
        }

        response = requests.request("POST", TOKEN_URL, data=request_body)
        new_token_info = response.json()

        session["access_token"] = new_token_info["access_token"]
        session["expires_at"] = (
            datetime.now().timestamp() + new_token_info["expires_in"]
        )

    return redirect("/playlists")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True)
