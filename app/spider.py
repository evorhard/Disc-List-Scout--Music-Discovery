from loguru import logger
from lxml import html
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


def request_rym(album_name: str) -> str:
    # https://rateyourmusic.com/search?searchterm=the%20soft%20moon&searchtype=
    # https://rateyourmusic.com/search?searchterm=the+soft+moon&searchtype=l

    album_name = album_name.replace(" ", "+")
    url = f"https://rateyourmusic.com/search?searchterm={album_name}&searchtype=l"

    response = make_request(url)

    with open("test_search.html", "w", encoding="utf-8") as f:
        f.write(response)

    return response


def process_rym(response: str):
    rym_tree = html.fromstring(response)
    first_result = rym_tree.xpath("//div[@class='page_search_results']//i[1]/a/@href")[
        0
    ]
    first_result_url = f"https://rateyourmusic.com{first_result}"

    logger.info(f"First result: {first_result_url}")

    first_result_list_url = f"{first_result_url}lists/"

    logger.info("Spidering the first page of list")

    album_list_response = make_request(first_result_list_url)

    with open("test_album_list.html", "w", encoding="utf-8") as f:
        f.write(album_list_response)


search_response = request_rym("the soft moon")
process_rym(search_response)
