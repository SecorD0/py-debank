from typing import Optional, List

import requests

from py_debank.models import Entrypoints, Curve
from py_debank.utils import get_proxy_dict, check_response, get_headers


def net_curve_24h(address: str, proxies: Optional[str or List[str]] = None) -> Curve:
    """
    Get an address's asset value history for the last 24 hours.

    Args:
        address (str): an address.
        proxies (Optional[str or List[str]]): an HTTP proxy or a proxy list for random choice for making
            a request. (None)

    Returns:
        Curve: the address's asset value history for the last 24 hours.

    """
    params = {
        'user_addr': address
    }
    response = requests.get(
        url=Entrypoints.PUBLIC.ASSET + 'net_curve_24h', params=params, headers=get_headers(),
        proxies=get_proxy_dict(proxies=proxies)
    )
    json_response = check_response(response=response)
    return Curve(data=json_response['data'])
