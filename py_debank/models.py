from dataclasses import dataclass
from typing import Optional, List

from pretty_utils.type_functions.classes import AutoRepr


@dataclass
class PublicAPI:
    ENTRYPOINT = 'https://api.debank.com/'
    ASSET = ENTRYPOINT + 'asset/'
    HISTORY = ENTRYPOINT + 'history/'
    NFT = ENTRYPOINT + 'nft/'
    PORTFOLIO = ENTRYPOINT + 'portfolio/'
    TOKEN = ENTRYPOINT + 'token/'
    USER = ENTRYPOINT + 'user/'


@dataclass
class V1API:
    ENTRYPOINT = 'https://pro-openapi.debank.com/v1/'


@dataclass
class Entrypoints:
    PUBLIC = PublicAPI
    V1 = V1API


@dataclass
class ChainNames:
    HECO = 'heco'
    MATIC = 'matic'
    ETHEREUM = 'eth'
    ARBITRUM = 'arb'
    AVALANCHE = 'avax'
    OPTIMISM = 'op'
    BSC = 'bsc'
    MOONBEAM = 'mobm'


@dataclass
class Mark:
    timestamp: int
    usd_value: float


class Curve(AutoRepr):
    def __init__(self, data: dict):
        usd_value_list = data.get('usd_value_list')
        self.persent_change: float = (usd_value_list[-1][1] / usd_value_list[0][1] - 1) * 100
        self.usd_change: float = usd_value_list[-1][1] - usd_value_list[0][1]
        self.marks: List[Mark] = []
        for mark in usd_value_list:
            self.marks.append(Mark(timestamp=mark[0], usd_value=mark[1]))


class Token(AutoRepr):
    def __init__(self, data: dict):
        self.chain: str = data.get('chain')
        self.symbol: str = data.get('symbol')
        self.usd_value: float = 0.0
        self.amount: Optional[float] = data.get('amount')
        self.price: Optional[float] = data.get('price')
        self.decimals: int = data.get('decimals')

        self.display_symbol: Optional[str] = data.get('display_symbol')
        self.id: id = data.get('id')
        self.is_core: bool = data.get('is_core')
        self.is_verified: bool = data.get('is_verified')
        self.is_wallet: bool = data.get('is_wallet')
        self.logo_url: str = data.get('logo_url')
        self.name: str = data.get('name')
        self.optimized_symbol: str = data.get('optimized_symbol')
        self.protocol_id: str = data.get('protocol_id')
        self.timestamp: Optional[float] = data.get('time_at')

        if self.amount and self.price:
            self.usd_value = self.amount * self.price


class PortfolioItem(AutoRepr):
    def __init__(self, data: dict):
        self.name: str = data.get('name')
        self.asset_usd_value: float = data.get('stats')['asset_usd_value']
        self.debt_usd_value: float = data.get('stats')['debt_usd_value']
        self.net_usd_value: float = data.get('stats')['net_usd_value']
        self.tokens: Optional[List[Token]] = None

        self.asset_dict: dict = data.get('asset_dict')
        self.detail_types: List[str] = data.get('detail_types')
        self.pool: dict = data.get('pool')
        self.position_index: Optional[str] = data.get('position_index')
        self.proxy_detail: dict = data.get('proxy_detail')
        self.update_at: float = data.get('update_at')

        details = data.get('details')
        if details:
            if 'supply_token_list' in details:
                self.parse_tokens(details['supply_token_list'])

            elif 'token' in details:
                self.parse_tokens([details['token']])

    def parse_tokens(self, tokens: list) -> None:
        if not tokens:
            return

        self.tokens = []
        for token in tokens:
            self.tokens.append(Token(data=token))

        self.tokens = sorted(self.tokens, key=lambda token: token.usd_value, reverse=True)


class Project(AutoRepr):
    def __init__(self, data: dict):
        self.chain: str = data.get('chain')
        self.name: str = data.get('name')
        self.site_url: str = data.get('site_url')
        self.tvl: float = data.get('tvl') if 'tvl' in data else 0.0
        self.usd_value: float = 0.0
        self.portfolio_item_list: Optional[List[PortfolioItem]] = None

        self.has_supported_portfolio: bool = data.get(
            'has_supported_portfolio') if 'has_supported_portfolio' in data else False
        self.id: str = data.get('id')
        self.is_tvl: bool = data.get('is_tvl') if 'is_tvl' in data else False
        self.is_visible_in_defi: bool = data.get('is_visible_in_defi') if 'is_visible_in_defi' in data else False
        self.logo_url: str = data.get('logo_url')
        self.platform_token_id: Optional[str] = data.get('platform_token_id')
        self.tag_ids: Optional[List[str]] = data.get('tag_ids')

        if 'portfolio_item_list' in data:
            self.parse_items(portfolio_item_list=data.get('portfolio_item_list'))

    def parse_items(self, portfolio_item_list: list) -> Optional[List[PortfolioItem]]:
        if not portfolio_item_list:
            return

        self.portfolio_item_list = []
        for portfolio_item in portfolio_item_list:
            portfolio_item = PortfolioItem(data=portfolio_item)
            self.usd_value += portfolio_item.asset_usd_value
            self.portfolio_item_list.append(portfolio_item)


class Collection(AutoRepr):
    def __init__(self, data: dict):
        self.chain: str = data.get('chain')
        self.name: str = data.get('name')
        self.id: str = data.get('id')
        self.nft_amount: Optional[int] = data.get('amount')
        self.spent_token: Optional[Token] = Token(data=data.get('spent_token')) if 'spent_token' in data else None
        self.avg_price_24h: float = data.get('avg_price_24h')
        self.avg_price_last_24h: float = data.get('avg_price_last_24h')
        self.floor_price: float = data.get('floor_price')
        self.floor_price_24h: float = data.get('floor_price_24h')
        self.max_price_24h: float = data.get('max_price_24h')
        self.max_price_last_24h: float = data.get('max_price_last_24h')
        self.volume_24h: float = data.get('volume_24h')
        self.volume_last_24h: float = data.get('volume_last_24h')

        self.description: Optional[str] = data.get('description')
        self.is_core: bool = data.get('is_core')
        self.is_visible: bool = data.get('is_visible')
        self.logo_url: str = data.get('logo_url')
        self.rank_at: int = data.get('rank_at')
        self.thirdparty: dict = data.get('thirdparty')


class NFT(AutoRepr):
    def __init__(self, data: dict, collection: Optional[Collection] = None):
        self.chain: str = data.get('chain')
        self.collection: Optional[Collection] = collection
        self.name: str = data.get('name')
        self.contract_id: Optional[str] = data.get('contract_id')
        self.usd_spent: float = 0.0
        self.amount: Optional[int] = data.get('amount')
        self.mint_gas_token: Optional[Token] = None
        self.mint_pay_token: Optional[Token] = None
        self.pay_token: Optional[Token] = None

        self.content: Optional[str] = data.get('content')
        self.content_type: Optional[str] = data.get('content_type')
        self.detail_url: Optional[str] = data.get('detail_url')
        self.id: str = data.get('id')
        self.inner_id: str = data.get('inner_id')
        self.minter: Optional[str] = data.get('minter')
        self.thumbnail_url: str = data.get('thumbnail_url')

        mint_gas_token = data.get('mint_gas_token')
        if mint_gas_token:
            self.mint_gas_token = Token(data=mint_gas_token)
            self.usd_spent += self.mint_gas_token.usd_value

        mint_pay_token = data.get('mint_pay_token')
        if mint_pay_token:
            self.mint_pay_token = Token(data=mint_pay_token)
            self.usd_spent += self.mint_pay_token.usd_value

        pay_token = data.get('pay_token')
        if pay_token and 'chain' in pay_token:
            self.pay_token = Token(data=pay_token)
            self.usd_spent += self.pay_token.usd_value


class Profit(AutoRepr):
    def __init__(self, data: dict):
        self.chain: str = data.get('chain')
        self.collection: Collection = Collection(data=data)
        self.usd_profit: float = 0.0
        self.profit: Optional[Token] = None
        self.spent: Optional[Token] = None
        self.revenue: Optional[Token] = None
        self.amount: int = data.get('amount')
        self.mint: int = data.get('mint_count')
        self.bought: int = data.get('buy_count')
        self.sold: int = data.get('sell_count')

        profit_token = data.get('profit_token')
        if profit_token:
            self.profit_token = Token(data=profit_token)
            self.usd_profit = self.profit_token.usd_value

        spent_token = data.get('spent_token')
        if spent_token:
            self.spent_token = Token(data=spent_token)

        revenue_token = data.get('revenue_token')
        if revenue_token:
            self.revenue_token = Token(data=revenue_token)


class ProfitLeaderboard(AutoRepr):
    def __init__(self, chain: str, profits: list):
        self.chain: str = chain
        self.usd_profit: float = 0.0
        self.profits: List[Profit] = []

        for profit in profits:
            profit = Profit(data=profit)
            self.profits.append(profit)
            self.usd_profit += profit.usd_profit


class Chain(AutoRepr):
    def __init__(self, name: str, tokens: Optional[list] = None, projects: Optional[list] = None,
                 collections: Optional[list] = None):
        self.name: str = name
        self.usd_value: float = 0.0
        self.tokens: Optional[List[Token]] = None
        self.projects: Optional[List[Project]] = None
        self.nfts: Optional[List[NFT]] = None

        self.parse_tokens(tokens=tokens)
        self.parse_projects(projects=projects)
        self.parse_nfts(collections=collections)

    def parse_tokens(self, tokens: list) -> None:
        if not tokens:
            return

        self.tokens = []
        for token in tokens:
            amount = token.get('amount')
            price = token.get('price')
            if amount and price:
                self.usd_value += amount * price

            self.tokens.append(Token(data=token))

        self.tokens = sorted(self.tokens, key=lambda token: token.usd_value, reverse=True)

    def parse_projects(self, projects: list) -> None:
        if not projects:
            return

        self.projects = []
        for project in projects:
            project = Project(data=project)
            self.usd_value += project.usd_value
            self.projects.append(project)

        self.projects = sorted(self.projects, key=lambda project: project.usd_value, reverse=True)

    def parse_nfts(self, collections: list) -> None:
        if not collections:
            return

        self.nfts = []
        for collection in collections:
            collection_instance = Collection(data=collection)
            for nft in collection.get('nft_list'):
                nft = NFT(data=nft, collection=collection_instance)
                self.nfts.append(nft)

        self.nfts = sorted(self.nfts, key=lambda nft: nft.usd_spent, reverse=True)


class NFTTx(AutoRepr):
    def __init__(self, chain: str, data: dict):
        self.chain: str = chain
        self.type: str = data.get('type')
        self.tx_id: str = data.get('tx_id')
        self.timestamp: float = data.get('time_at')
        self.address: str = data.get('user_addr')
        self.nft: NFT = NFT(data=data.get('nft'), collection=Collection(data=data.get('collection')))
        self.pay_token: Token = Token(data=data.get('pay_token'))

        self.id: str = data.get('id')


class NFTHistory(AutoRepr):
    def __init__(self, chain: str, address: str, data: dict):
        self.chain: str = chain
        self.address: str = address
        self.txs: Optional[List[AutoRepr]] = None

        self.parse_txs(data=data)

    def parse_txs(self, data: dict) -> None:
        txs = data.get('history_list')
        if not txs:
            return

        self.txs = []
        for tx in txs:
            self.txs.append(NFTTx(chain=self.chain, data=tx))


class Tx(AutoRepr):
    def __init__(self, data: dict):
        self.chain: str = data.get('chain')
        self.type: str = data.get('cate_id')
        self.tx_id: str = data.get('id')
        self.timestamp: float = data.get('time_at')
        self.sender: Optional[str] = None
        self.recipient: Optional[str] = None
        self.receives: Optional[List[Token, NFT]] = None
        self.sends: Optional[List[Token, NFT]] = None
        self.token_approve: Optional[Token] = None
        self.eth_gas_fee: Optional[float] = None
        self.usd_gas_fee: Optional[float] = None
        self.project: Optional[Project] = None

        tx = data.get('tx')
        if tx:
            if not self.type:
                self.type: str = tx['name']

            self.sender = tx['from_addr']
            self.recipient = tx['to_addr']

            self.eth_gas_fee = tx['eth_gas_fee']
            self.usd_gas_fee = tx['usd_gas_fee']

        if self.type == 'receive':
            self.sender = data.get('other_addr')
            self.recipient = data.get('address')

        elif self.type == 'send':
            self.sender = data.get('address')
            self.recipient = data.get('other_addr')

        token_dict = data.get('token_dict')
        receives = data.get('receives')
        if receives:
            self.receives = []
            for item in receives:
                token = token_dict.get(item.get('token_id'))
                token['amount'] = item.get('amount')
                # if 'price' in token and token['price'] is None:
                #     token['price'] = 0.0

                try:
                    token = Token(data=token)

                except:
                    pay_token = token.get('pay_token')
                    if pay_token:
                        token['pay_token'] = token_dict.get(pay_token.get('id'))

                    token = NFT(data=token)

                token.amount = item.get('amount')
                self.receives.append(token)

        sends = data.get('sends')
        if sends:
            self.sends = []
            for item in sends:
                token = token_dict.get(item.get('token_id'))
                token['amount'] = item.get('amount')
                # if 'price' in token and token['price'] is None:
                #     token['price'] = 0.0

                try:
                    token = Token(data=token)

                except:
                    pay_token = token.get('pay_token')
                    if pay_token:
                        token['pay_token'] = token_dict.get(pay_token.get('id'))

                    token = NFT(data=token)

                token.amount = item.get('amount')
                self.sends.append(token)

        token_approve = data.get('token_approve')
        if token_approve:
            token = token_dict.get(token_approve.get('token_id'))
            token['amount'] = token_approve.get('value')
            self.token_approve = Token(data=token)

        project_id = data.get('project_id')
        if project_id:
            self.project = Project(data=data.get('project_dict')[project_id])


class History(AutoRepr):
    def __init__(self, address: str, data: dict):
        self.address: str = address.lower()
        self.txs: Optional[List[AutoRepr]] = None

        self.parse_txs(address=self.address, data=data)

    def parse_txs(self, address: str, data: dict) -> None:
        txs = data.get('history_list')
        if not txs:
            return

        self.txs = []
        for tx in txs:
            tx.update({'address': address, 'project_dict': data.get('project_dict'),
                       'token_dict': data.get('token_dict')})
            self.txs.append(Tx(data=tx))


class User(AutoRepr):
    def __init__(self, data: dict):
        self.account_id: Optional[str] = data.get('account_id')
        self.avatar: Optional[str] = data.get('avatar')
        self.comment: Optional[str] = data.get('comment')
        self.create_at: int = data.get('create_at')
        self.email_verified: bool = data.get('email_verified')
        self.follower_count: int = data.get('follower_count')
        self.following_count: int = data.get('following_count')
        self.id: str = data.get('id')
        self.is_contract: bool = data.get('is_contract')
        self.is_editor: bool = data.get('is_editor')
        self.is_followed: bool = data.get('is_followed')
        self.is_following: bool = data.get('is_following')
        self.is_mine: bool = data.get('is_mine')
        self.is_mirror_author: bool = data.get('is_mirror_author')
        self.is_multisig_addr: bool = data.get('is_multisig_addr')
        self.market_status: Optional[str] = data.get('market_status')
        self.org: dict = data.get('org')
        self.protocol_usd_value: float = data.get('protocol_usd_value')
        self.relation: Optional[str] = data.get('relation')
        self.tvf: float = data.get('tvf')
        self.usd_value: float = data.get('usd_value')
        self.used_chains: List[str] = data.get('used_chains')
        self.wallet_usd_value: float = data.get('wallet_usd_value')


class Info(AutoRepr):
    def __init__(self, data: dict):
        self.create_at: Optional[float] = data.get('create_at')
        self.id: str = data.get('id')
        self.initial_price: int = data.get('initial_price')
        self.offer_price: int = data.get('offer_price')
        self.replied_rate: float = data.get('replied_rate')
        self.uncharged_offer_count: int = data.get('uncharged_offer_count')
        self.uncharged_offer_value: int = data.get('uncharged_offer_value')
        self.unread_message_count: int = data.get('unread_message_count')
        self.user: User = User(data=data.get('user'))
