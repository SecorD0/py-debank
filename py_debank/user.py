from typing import Optional, List

import requests

from py_debank.models import Info, User, Entrypoints
from py_debank.utils import get_proxy_dict, check_response, get_headers


def addr(address: str, proxies: Optional[str or List[str]] = None) -> User:
    """
    Get a DeBank user.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        User: the DeBank user.

    """
    params = {
        'addr': address
    }
    response = requests.get(
        url=Entrypoints.PUBLIC.USER + 'addr', params=params, headers=get_headers(),
        proxies=get_proxy_dict(proxies=proxies)
    )
    json_response = check_response(response=response)
    return User(data=json_response['data'])


def info(address: str, proxies: Optional[str or List[str]] = None) -> Info:
    """
    Get an information about a DeBank user.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Info: the information about the DeBank user.

    """
    params = {
        'id': address
    }
    response = requests.get(
        url=Entrypoints.PUBLIC.ENTRYPOINT + 'hi/user/info', params=params, headers=get_headers(),
        proxies=get_proxy_dict(proxies=proxies)
    )
    json_response = check_response(response=response)
    return Info(data=json_response['data'])


def total_balance(address: str, proxies: Optional[str or List[str]] = None) -> float:
    """
    Get a total balance of an address.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        float: the total balance.

    """
    params = {
        'addr': address
    }
    response = requests.get(
        url=Entrypoints.PUBLIC.USER + 'total_balance', params=params, headers=get_headers(),
        proxies=get_proxy_dict(proxies=proxies)
    )
    json_response = check_response(response=response)
    return json_response['data']['total_usd_value']
