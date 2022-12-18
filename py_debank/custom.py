from typing import Dict, Optional, List

from py_debank import nft
from py_debank import portfolio
from py_debank import token
from py_debank.models import Chain, ChainNames


def get_balance(address: str, chain: ChainNames or str = '', parse_nfts: bool = True,
                proxies: Optional[str or List[str]] = None) -> Dict[str, Chain]:
    """
    Get the following information of an address of one or all chains:
    - token balances
    - projects where the account's assets are located
    - owned NFTs

    :param str address: the address
    :param ChainNames or st chain: the chain (all chains)
    :param bool parse_nfts: whether to parse NFT, it leads to a high probability of "429 Too Many Requests" error (True)
    :param Optional[str or List[str]] proxies: an HTTP proxy or a proxy list for random choice for making a request (None)
    :return Chain: the address information
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
        tokens = token.cache_balance_list(address=address, proxies=proxies)
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
