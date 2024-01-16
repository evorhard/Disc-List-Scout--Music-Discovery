import requests

from loguru import logger


def make_request(url: str) -> requests.Response:
    response = requests.request("GET", url, timeout=300)

    return response


def spider_discogs(album_name: str):
    album_name = album_name.replace(" ", "+")
    url = f"https://www.discogs.com/search?q={album_name}&type=all"

    response = make_request(url)

    logger.info(response.text)


spider_discogs("saw you for the first time")
