from pretty_utils.miscellaneous.files import touch, read_lines
from pretty_utils.miscellaneous.time_and_date import unix_to_strtime

from py_debank import asset, history, nft, portfolio, token, user, custom
from py_debank.models import ChainNames


class Asset:
    @staticmethod
    def net_curve_24h(address: str) -> None:
        curve = asset.net_curve_24h(address=address, proxies=proxies)
        print(f'{curve.persent_change=}\n{curve.usd_change=}')
        for mark in curve.marks:
            print(mark)


class History:
    @staticmethod
    def list_(address: str) -> None:
        for tx in history.list_(address=address, page_count=21, proxies=proxies).txs:
            print(tx)

        print('----------------------------------------------------------------------------')

    @staticmethod
    def token_price(token_id: str, chain: ChainNames or str):
        print(f'Current price: ${history.token_price(token_id=token_id, chain=chain)}')
        time_at = 1637275496
        print(
            f'Price at {unix_to_strtime(time_at)}: ${history.token_price(token_id=token_id, chain=chain, time_at=time_at)}')


class NFT:
    @staticmethod
    def collection_list(address: str, chain: ChainNames or str = '') -> None:
        for key, value in nft.collection_list(address=address, chain=chain, proxies=proxies).items():
            print(f'\n-------------------------------- {key} --------------------------------')
            for chain_nft in value.nfts:
                print(f'{chain_nft}\n')

    @staticmethod
    def history_collection_list(address: str, chain: ChainNames or str = '') -> None:
        for key, value in nft.history_collection_list(address=address, chain=chain, proxies=proxies).items():
            print(f'\n-------------------------------- {key} --------------------------------')
            print(f'{value.usd_profit=}')
            for profit in value.profits:
                print(f'{profit}\n')

    @staticmethod
    def history_list(address: str, chain: ChainNames or str = '') -> None:
        for key, value in nft.history_list(address=address, chain=chain, proxies=proxies).items():
            print(f'\n-------------------------------- {key} --------------------------------')
            for tx in value.txs:
                print(f'{tx}\n')

    @staticmethod
    def used_chains(address: str) -> None:
        print(nft.used_chains(address=address, proxies=proxies))


class Portfolio:
    @staticmethod
    def project_list(address: str) -> None:
        for key, value in portfolio.project_list(address=address, proxies=proxies).items():
            print(f'\n-------------------------------- {key} --------------------------------')
            for project in value.projects:
                print(f'{project}')
                for portfolio_item in project.portfolio_item_list:
                    print(f'\t{portfolio_item}')
                    for token in portfolio_item.tokens:
                        print(f'\t\t{token}')


class Token:
    @staticmethod
    def balance_list(address: str, chain: ChainNames or str) -> None:
        balance = token.balance_list(address=address, chain=chain, proxies=proxies)
        print(f'{balance.usd_value=}')
        for chain_token in balance.tokens:
            print(f'{chain_token}\n')

    @staticmethod
    def cache_balance_list(address: str) -> None:
        for key, value in token.cache_balance_list(address=address, proxies=proxies).items():
            print(f'\n-------------------------------- {key} --------------------------------')
            for chain_token in value.tokens:
                print(f'{chain_token}\n')


class User:
    @staticmethod
    def addr(address: str) -> None:
        print(user.addr(address=address, proxies=proxies))

    @staticmethod
    def info(address: str) -> None:
        print(user.info(address=address, proxies=proxies))

    @staticmethod
    def total_balance(address: str) -> None:
        print(user.total_balance(address=address, proxies=proxies))


class Custom:
    @staticmethod
    def get_balance(address: str, chain: ChainNames or str = '') -> None:
        for key, value in custom.get_balance(address=address, chain=chain, proxies=proxies).items():
            print(
                f'\n-------------------------------- {key} (${round(value.usd_value, 2)}) --------------------------------')
            if value.tokens:
                print('Tokens:')
                for chain_token in value.tokens:
                    print(f'\t{chain_token}')

            if value.projects:
                print('---\nProjects:')
                for project in value.projects:
                    print(f'\n\t{project}')
                    for portfolio_item in project.portfolio_item_list:
                        print(f'\t\t{portfolio_item}')
                        for token in portfolio_item.tokens:
                            print(f'\t\t\t{token}')

            if value.nfts:
                print('---\nNFTs:')
                for chain_nft in value.nfts:
                    print(f'\t{chain_nft}')

    @staticmethod
    def current_balance_list(address: str) -> None:
        for key, value in custom.current_balance_list(address=address, proxies=proxies).items():
            print(f'\n-------------------------------- {key} --------------------------------')
            for chain_token in value.tokens:
                print(f'{chain_token}\n')


def main() -> None:
    print('\n--------- Asset ---------')
    asset_cls = Asset()
    asset_cls.net_curve_24h(address=checking_address)

    print('\n--------- History ---------')
    history_cls = History()
    history_cls.list_(address=checking_address)
    history_cls.token_price(token_id='0xB8c77482e45F1F44dE1745F52C74426C631bDD52', chain=ChainNames.ETHEREUM)

    print('\n--------- NFT ---------')
    nft_cls = NFT()
    nft_cls.collection_list(address=checking_address, chain=ChainNames.ARBITRUM)
    nft_cls.collection_list(address=checking_address)
    nft_cls.history_collection_list(address=checking_address, chain='arb')
    nft_cls.history_collection_list(address=checking_address)
    nft_cls.history_list(address=checking_address, chain=ChainNames.ARBITRUM)
    nft_cls.used_chains(address=checking_address)

    print('\n--------- Portfolio ---------')
    portfolio_cls = Portfolio()
    portfolio_cls.project_list(address=checking_address)

    print('\n--------- Token ---------')
    token_cls = Token()
    token_cls.balance_list(address=checking_address, chain='arb')
    token_cls.cache_balance_list(address=checking_address)

    print('\n--------- User ---------')
    user_cls = User()
    user_cls.addr(address=checking_address)
    user_cls.info(address=checking_address)
    user_cls.total_balance(address=checking_address)

    print('\n--------- Custom ---------')
    custom_cls = Custom()
    custom_cls.get_balance(address=checking_address, chain=ChainNames.ARBITRUM)
    custom_cls.get_balance(address=checking_address)
    custom_cls.current_balance_list(address=checking_address)


if __name__ == '__main__':
    touch('proxies.txt', True)
    proxies = read_lines('proxies.txt', True)
    checking_address = '0x15B328F211B7a9387CA4da4a6DB4990eAF37b1b4'  # It's a random address from the explorer

    main()
