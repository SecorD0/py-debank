from typing import Optional, List

import requests

from py_debank.models import Entrypoints, History, ChainNames
from py_debank.utils import get_proxy_dict, check_response, get_headers


def list_(
        address: str, chain: ChainNames or str = '', start_time: int or str = 0, page_count: int or str = 20,
        proxies: Optional[str or List[str]] = None
) -> History:
    """
    Get a transaction history of an address.

    :param str address: the address
    :param ChainNames or str chain: a chain (all chains)
    :param int or str start_time: before what time to parse transactions (0)
    :param int or str page_count: how many recent transactions to parse (20)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return History: the transaction history
    """
    data = {}
    if page_count <= 20:
        params = {
            'user_addr': address,
            'chain': chain,
            'start_time': str(start_time),
            'page_count': str(page_count)
        }
        response = requests.get(
            url=Entrypoints.PUBLIC.HISTORY + 'list', params=params, headers=get_headers(),
            proxies=get_proxy_dict(proxies=proxies)
        )
        json_response = check_response(response=response)
        data = json_response['data']

    else:
        page_counts = [20] * (page_count // 20)
        page_counts.append(page_count - len(page_counts) * 20)
        for page_count in page_counts:
            params = {
                'user_addr': address,
                'chain': chain,
                'start_time': str(start_time),
                'page_count': str(page_count)
            }
            response = requests.get(
                url=Entrypoints.PUBLIC.HISTORY + 'list', params=params, headers=get_headers(),
                proxies=get_proxy_dict(proxies=proxies)
            )
            json_response = check_response(response=response)
            if data:
                data['history_list'] += json_response['data']['history_list']
                data['project_dict'].update(json_response['data']['project_dict'])
                data['token_dict'].update(json_response['data']['token_dict'])

            else:
                data = json_response['data']

            start_time = int(data['history_list'][-1]['time_at'])

    return History(address=address, data=data)


def token_price(
        token_id: str, chain: ChainNames or str, time_at: Optional[int or str] = None,
        proxies: Optional[str or List[str]] = None
) -> float:
    """
    Get a token price at a certain point in time.

    :param str token_id: the token contract address or the coin name
    :param ChainNames or str chain: a chain
    :param Optional[int or str] time_at: at what point in time to get a token price (current time)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return float: the token price
    """
    params = {
        'chain': chain,
        'token_id': token_id
    }
    if time_at:
        params['time_at'] = time_at

    response = requests.get(
        url=Entrypoints.PUBLIC.HISTORY + 'token_price', params=params, headers=get_headers(),
        proxies=get_proxy_dict(proxies=proxies)
    )
    json_response = check_response(response=response)
    return json_response['data']['price']
