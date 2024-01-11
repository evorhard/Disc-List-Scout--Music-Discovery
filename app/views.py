from flask import Blueprint

views_blueprint = Blueprint("views", __name__)


@views_blueprint.route("/")
def index():
    return "Welcome to my Spotify App <a href='/login'>Login with Spotify</a>"
