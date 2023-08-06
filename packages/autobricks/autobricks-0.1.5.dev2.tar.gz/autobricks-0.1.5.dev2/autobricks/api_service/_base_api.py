import requests
from requests.exceptions import HTTPError
from . import autobricks_logging
import os

_logger = autobricks_logging.get_logger(__name__)

_ssl_verify = False if os.getenv("SSL_VERIFY", "false").lower() == "false" else True
if not _ssl_verify:
    _logger.info(f"WARNING SSL Verification is off!")

def base_api_get(
    url: str, headers: dict, json: dict = None, data: dict = None, query: str = None
):

    if query:
        url = f"{url}?{query}"
    response = requests.get(url=url, headers=headers, json=json, data=data, verify=_ssl_verify)

    try:
        response.raise_for_status()

    except HTTPError as e:

        msg = f"{e.response.status_code} error at {url} {e.response.text}"
        _logger.error(msg)
        raise e

    return response


def base_api_post(url: str, headers: dict, json: dict = None, data: dict = None):

    response = requests.post(url=url, headers=headers, json=json, data=data, verify=_ssl_verify)

    try:
        response.raise_for_status()

    except HTTPError as e:

        msg = f"{e.response.status_code} error at {url} {e.response.text}"
        _logger.error(msg)
        raise e

    return response
