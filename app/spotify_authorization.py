import requests

from collections import namedtuple
from typing import Dict

User = namedtuple("User", ["id", "display_name"])


def exchange_code_for_token(
    code: str, client_id: str, client_secret: str, redirect_uri: str, token_url: str
) -> Dict:
    """Takes the authorization information and exchanges it for a token

    Arguments:
        code {str} -- spotify's "code"
        client_id {str} -- the client's id
        client_secret {str} -- the client's secret
        redirect_uri {str} -- the redirect uri
        token_url {str} -- the url needed for a token

    Returns:
        Dict -- The token information retrieved
    """
    request_body = {
        "code": code,
        "grant_type": "authorization_code",
        "redirect_uri": redirect_uri,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.post(token_url, data=request_body)
    token_info = response.json()

    return token_info


def get_user_information(access_token: str, api_base_url: str) -> str:
    """Gets the user id needed to retrieve the playlists

    Arguments:
        access_token {str} -- access token needed to access user information such as playlists
        api_base_url {str} -- the base api endpoint

    Returns:
        str -- the user's id
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.request("GET", f"{api_base_url}/me", headers=headers)
    user_info = response.json()

    user = User(id=user_info["id"], display_name=user_info["display_name"])

    return user


def get_user_playlist(access_token: str, api_base_url: str, user_id: str) -> Dict:
    """Gets the users playlist in json format

    Arguments:
        access_token {str} -- access token needed to access user information such as playlists
        api_base_url {str} -- the base api endpoint
        user_id {str} -- the user's id

    Returns:
        Dict -- playlists in json format
    """
    headers = {"Authorization": f"Bearer {access_token}"}

    response = requests.request(
        "GET", f"{api_base_url}/users/{user_id}/playlists", headers=headers
    )
    playlists = response.json()

    return playlists


def refresh_token(
    refresh_token: str, client_id: str, client_secret: str, token_url: str
) -> Dict:
    """Refreshes the token if the token expires

    Arguments:
        refresh_token {str} -- the user's refresh token
        client_id {str} -- the client's id
        client_secret {str} -- the client's secret
        token_url {str} -- the url needed for a token

    Returns:
        Dict -- a json with information for a new token
    """
    request_body = {
        "grant_type": "refresh_token",
        "refresh_token": refresh_token,
        "client_id": client_id,
        "client_secret": client_secret,
    }

    response = requests.request("POST", token_url, data=request_body)
    new_token_info = response.json()

    return new_token_info
