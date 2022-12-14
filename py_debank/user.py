from typing import Optional, List

import requests

from py_debank.models import Info, User, Entrypoints
from py_debank.utils import get_proxy_dict, check_response, get_headers


def addr(address: str, proxies: Optional[str or List[str]] = None) -> User:
    """
    Get a DeBank user.

    :param str address: an address
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return User: the DeBank user
    """
    params = {'addr': address}
    response = requests.get(Entrypoints.PUBLIC.USER + 'addr', params=params, headers=get_headers(),
                            proxies=get_proxy_dict(proxies=proxies))
    json_dict = check_response(response=response)
    return User(data=json_dict['data'])


def info(address: str, proxies: Optional[str or List[str]] = None) -> Info:
    """
    Get an information about a DeBank user.

    :param str address: an address
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Info: the information about the DeBank user
    """
    params = {'id': address}
    response = requests.get(Entrypoints.PUBLIC.ENTRYPOINT + 'hi/user/info', params=params, headers=get_headers(),
                            proxies=get_proxy_dict(proxies=proxies))
    json_dict = check_response(response=response)
    return Info(data=json_dict['data'])


def total_balance(address: str, proxies: Optional[str or List[str]] = None) -> float:
    """
    Get a total balance of an address.

    :param str address: the address
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return float: the total balance
    """
    params = {'addr': address}
    response = requests.get(Entrypoints.PUBLIC.USER + 'total_balance', params=params, headers=get_headers(),
                            proxies=get_proxy_dict(proxies=proxies))
    json_dict = check_response(response=response)
    return json_dict['data']['total_usd_value']
