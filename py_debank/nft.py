import time
from typing import Optional, List, Dict

import requests

from py_debank.models import Entrypoints, ChainNames, Chain, ProfitLeaderboard, NFTHistory
from py_debank.utils import get_proxy_dict, check_response, get_headers


def collection_list(
        address: str, chain: ChainNames or str = '', raw_data: bool = False, proxies: Optional[str or List[str]] = None
) -> Dict[str, Chain] or Dict[str, dict]:
    """
    Get owned collections (raw data) or NFTs by an address.

    Args:
        address (str): an address.
        chain (ChainNames or str): a chain. (all chains)
        raw_data (bool): if True, it will return the unprocessed dictionary. (False)
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Dict[str, Chain] or Dict[str, dict]: owned collections (raw data) or NFTs.
        ::

            {
                'eth': Chain(..., nfts=...),
                'bsc': Chain(..., nfts=...)
            }

    """
    chain_dict = {}
    if chain:
        proxy_dict = get_proxy_dict(proxies=proxies)
        for i in range(3):
            params = {
                'user_addr': address,
                'chain': chain
            }
            response = requests.get(
                url=Entrypoints.PUBLIC.NFT + 'collection_list', params=params, headers=get_headers(), proxies=proxy_dict
            )
            json_response = check_response(response=response)
            if json_response['data']['job']:
                time.sleep(3)

            else:
                chain_dict[chain] = json_response['data']['result']['data']
                break

    else:
        chains = used_chains(address=address, proxies=proxies)
        for chain in chains:
            proxy_dict = get_proxy_dict(proxies=proxies)
            for i in range(3):
                params = {
                    'user_addr': address,
                    'chain': chain
                }
                response = requests.get(
                    url=Entrypoints.PUBLIC.NFT + 'collection_list', params=params, headers=get_headers(),
                    proxies=proxy_dict
                )
                json_response = check_response(response=response)
                if json_response['data']['job']:
                    time.sleep(3)

                else:
                    chain_dict[chain] = json_response['data']['result']['data']
                    break

    if not raw_data:
        chain_list = [Chain(name=name, collections=collections) for name, collections in chain_dict.items()]
        chain_dict = {}
        for chain in sorted(chain_list, key=lambda chain: chain.usd_value, reverse=True):
            chain_dict[chain.name] = chain

    return chain_dict


def history_collection_list(
        address: str, chain: ChainNames or str = '', proxies: Optional[str or List[str]] = None
) -> Dict[str, ProfitLeaderboard]:
    """
    Get a profit leaderboard for all the NFT collections the address has ever owned.

    Args:
        address (str): an address.
        chain (ChainNames or str): a chain. (all chains)
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Dict[str, List[ProfitLeaderboard]]: the profit leaderboard.
        ::

            {
                'eth': ProfitLeaderboard(...),
                'bsc': ProfitLeaderboard(...)
            }

    """
    profit_dict = {}
    if chain:
        proxy_dict = get_proxy_dict(proxies=proxies)
        for i in range(3):
            params = {
                'user_addr': address,
                'chain': chain
            }
            response = requests.get(
                url=Entrypoints.PUBLIC.NFT + 'history_collection_list', params=params, headers=get_headers(),
                proxies=proxy_dict
            )
            json_response = check_response(response=response)
            if json_response['data']['job']:
                time.sleep(3)

            else:
                profit_dict[chain] = json_response['data']['result']['data']
                break

    else:
        chains = used_chains(address=address, proxies=proxies)
        for chain in chains:
            proxy_dict = get_proxy_dict(proxies=proxies)
            for i in range(3):
                params = {
                    'user_addr': address,
                    'chain': chain
                }
                response = requests.get(
                    url=Entrypoints.PUBLIC.NFT + 'history_collection_list', params=params, headers=get_headers(),
                    proxies=proxy_dict
                )
                json_response = check_response(response=response)
                if json_response['data']['job']:
                    time.sleep(3)

                else:
                    profit_dict[chain] = json_response['data']['result']['data']
                    break

    profit_list = []
    for name, data in profit_dict.items():
        if data:
            profit_list.append(ProfitLeaderboard(chain=name, profits=data))

    profit_dict = {}
    for profit in sorted(profit_list, key=lambda profit: profit.usd_profit, reverse=True):
        profit_dict[profit.chain] = profit

    return profit_dict


def history_list(
        address: str, chain: ChainNames or str = '', proxies: Optional[str or List[str]] = None
) -> Dict[str, NFTHistory] or Dict[str, dict]:
    """
    Get a NFT transaction history of an address.

    Args:
        address (str): an address.
        chain (ChainNames or str): a chain. (all chains)
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Dict[str, NFTHistory] or Dict[str, dict]: the NFT transaction history.
        ::

            {
                'eth': NFTHistory(...),
                'bsc': NFTHistory(...)
            }

    """
    history_dict = {}
    if chain:
        params = {
            'user_addr': address,
            'chain': chain,
            'type': '',
            'anchor_time': '',
            'anchor_id': '',
            'page_count': '20',
            'direction': ''
        }
        response = requests.get(
            url=Entrypoints.PUBLIC.NFT + 'history_list', params=params, headers=get_headers(),
            proxies=get_proxy_dict(proxies=proxies)
        )
        json_response = check_response(response=response)
        history_dict[chain] = NFTHistory(chain=chain, address=address, data=json_response['data'])

    else:
        chains = used_chains(address=address, proxies=proxies)
        for chain in chains:
            params = {
                'user_addr': address,
                'chain': chain,
                'type': '',
                'anchor_time': '',
                'anchor_id': '',
                'page_count': '20',
                'direction': ''
            }
            response = requests.get(
                url=Entrypoints.PUBLIC.NFT + 'history_list', params=params, headers=get_headers(),
                proxies=get_proxy_dict(proxies=proxies)
            )
            json_response = check_response(response=response)
            history_dict[chain] = NFTHistory(chain=chain, address=address, data=json_response['data'])

    return history_dict


def used_chains(address: str, proxies: Optional[str or List[str]] = None) -> List[str]:
    """
    Get chains in which there was interaction with NFT.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        List[str]: chains.

    """
    params = {
        'user_addr': address
    }
    response = requests.get(
        url=Entrypoints.PUBLIC.NFT + 'used_chains', params=params, headers=get_headers(),
        proxies=get_proxy_dict(proxies=proxies)
    )
    json_response = check_response(response=response)
    return json_response['data']
