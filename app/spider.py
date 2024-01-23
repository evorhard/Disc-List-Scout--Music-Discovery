from loguru import logger
from typing import Dict
from zenrows import ZenRowsClient

# Local imports
from config import ZEN_ROWS


def make_request(
    url: str, timeout: int = 60, headers: Dict = None, data: Dict = None
) -> str:
    client = ZenRowsClient(ZEN_ROWS)
    params = {"js_render": "true", "premium_proxy": "true"}

    response = client.get(url, timeout=timeout, params=params)

    logger.info(response.status_code)

    return response.text


def spider_rym(album_name: str):
    # https://rateyourmusic.com/search?searchterm=the%20soft%20moon&searchtype=
    # https://rateyourmusic.com/search?searchterm=the+soft+moon&searchtype=l

    album_name = album_name.replace(" ", "+")
    url = f"https://rateyourmusic.com/search?searchterm={album_name}&searchtype=l"

    response = make_request(url)

    with open("test.html", "w", encoding="utf-8") as f:
        f.write(response)


spider_rym("the soft moon")
