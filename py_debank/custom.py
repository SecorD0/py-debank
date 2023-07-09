from typing import Dict, Optional, List

from py_debank import nft
from py_debank import portfolio
from py_debank import token
from py_debank.models import Chain, ChainNames
from py_debank.token import balance_list
from py_debank.user import addr


def get_balance(
        address: str, chain: ChainNames or str = '', parse_nfts: bool = True, proxies: Optional[str or List[str]] = None
) -> Dict[str, Chain]:
    """
    Get the following information of an address of one or all chains:

    - token balances
    - projects where the account's assets are located
    - owned NFTs

    Args:
        address (str): an address.
        chain (ChainNames or str): a chain. (all chains)
        parse_nfts (bool): whether to parse NFT, it leads to a high probability of "429 Too Many Requests" error. (True)
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Chain: the address information.

    """
    chains: Dict[str, Chain] = {}
    if chain:
        tokens = token.balance_list(address=address, chain=chain, proxies=proxies)
        chains.update({chain: tokens})

        if parse_nfts:
            nfts = nft.collection_list(address=address, chain=chain, raw_data=True, proxies=proxies)
            if nfts:
                chains[chain].parse_nfts(nfts[chain])

        projects = portfolio.project_list(address=address, raw_data=True, proxies=proxies)
        if chain in projects:
            chains[chain].parse_projects(projects[chain])

    else:
        tokens = current_balance_list(address=address, proxies=proxies)
        chains.update(tokens)

        if parse_nfts:
            nfts = nft.collection_list(address=address, raw_data=True, proxies=proxies)
            for name, nft_dict in nfts.items():
                if name in chains:
                    chains[name].parse_nfts(nft_dict)

                else:
                    chains[name] = Chain(name=name, tokens=nft_dict)

        projects = portfolio.project_list(address=address, raw_data=True, proxies=proxies)
        for name, project_dict in projects.items():
            if name in chains:
                chains[name].parse_projects(project_dict)

            else:
                chains[name] = Chain(name=name, projects=project_dict)

    chains = {key: value for key, value in sorted(chains.items(), key=lambda item: item[1].usd_value, reverse=True)}
    return chains


def current_balance_list(
        address: str, raw_data: bool = False, proxies: Optional[str or List[str]] = None
) -> Dict[str, Chain] or Dict[str, dict]:
    """
    Get current token balances of an address of all chains.

    Args:
        address (str): an address.
        raw_data: if True, it will return the unprocessed dictionary. (False)
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Dict[str, Chain] or Dict[str, dict]: token balances.
        ::

            {
                'eth': Chain(..., tokens=...),
                'bsc': Chain(..., tokens=...)
            }

    """
    chain_dict = {}
    used_chains = addr(address=address, proxies=proxies).used_chains
    for chain in used_chains:
        balance = balance_list(address=address, chain=chain, raw_data=raw_data, proxies=proxies)
        if balance.tokens:
            chain_dict[chain] = balance

    if not raw_data:
        chain_dict = {
            key: value for key, value in sorted(chain_dict.items(), key=lambda item: item[1].usd_value, reverse=True)
        }

    return chain_dict
