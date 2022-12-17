import random
from typing import Optional, List

import requests
from fake_useragent import UserAgent

from py_debank import exceptions


def get_headers() -> dict:
    """
    Get headers for a request.

    :return dict: headers
    """
    return {
        'accept': '*/*',
        'accept-language': 'en-US,en;q=0.9',
        'origin': 'https://debank.com',
        'referer': 'https://debank.com/',
        'source': 'web',
        'user-agent': UserAgent().chrome
    }


def get_proxy_dict(proxies: Optional[str or List[str]] = None) -> Optional[dict]:
    """
    Construct a proxy dictionary for use in the 'requests' library.

    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Optional[dict]: the proxy dictionary with the selected proxy
    """
    if not proxies:
        return

    if isinstance(proxies, str):
        proxy = proxies

    elif isinstance(proxies, list):
        proxy = random.choice(proxies)

    else:
        return

    if 'http' not in proxy:
        proxy = f'http://{proxy}'

    return {'http': proxy, 'https': proxy}


def check_response(response: requests.Response) -> dict:
    """
    Check if a request was sent successfully.

    :param requests.Response response: the response instance
    :return dict: the json-encoded content of a response
    """
    status_code = response.status_code
    if status_code != requests.codes.ok:
        raise exceptions.DebankException(status_code=status_code)

    response = response.json()
    if response['error_code']:
        raise exceptions.DebankException(status_code=status_code, error_msg=response['error_msg'])

    return response
