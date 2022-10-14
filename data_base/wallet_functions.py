import requests
from bipwallet import wallet
from bipwallet.utils import *
from bit import PrivateKey


def create_wallet(coin):
    # generate 12 word mnemonic seed
    seed = wallet.generate_mnemonic()

    # create bitcoin wallet
    w = wallet.create_wallet(network='TRC', seed=seed, children=3)
    return w


def gen_address(index):
    # Наша seed фраза
    seed = 'during style topic antenna east alien next umbrella mansion bitter dinner merry'

    # Мастер ключ из seed фразы
    master_key = HDPrivateKey.master_key_from_mnemonic(seed)

    # Public key из мастер ключа по пути 'm/44/0/0/0'
    root_keys = HDKey.from_path(master_key, "m/44'/195'/0'/0/0")[-1].public_key.to_b58check()

    # Extended public key
    xpublic_key = str(root_keys)

    # Адрес дочернего кошелька в зависимости от значения index
    address = Wallet.deserialize(xpublic_key, network='BTC').get_child(index, is_prime=False).to_address()

    rootkeys_wif = HDKey.from_path(master_key, f"m/44'/195'/0'/0/{index}")[-1]

    # Extended private key
    xprivatekey = str(rootkeys_wif.to_b58check())

    # Wallet import format
    wif = Wallet.deserialize(xprivatekey, network='BTC').export_to_wif()

    return address, wif


def check_wallet_value(wallet):
    # Адрес кошелька пользователя

    # wallet = gen_address(0)
    url = f'https://blockchain.info/rawaddr/{wallet}'
    x = requests.get(url)
    wallet = x.json()

    return wallet['final_balance'], wallet['txs']


# ('164r7cuiBjC8dLpPPu7ykjuunMSwpwak6J', 'L47tp1ikAi4ReJJPymCc5hRpkVDhmyomoDJEicn6qw5rhRJXJqRh')
# {'coin': 'BTC', 'seed': 'derive they parade card trip crawl junk utility crash claim copy neck',
# 'private_key': 'a190f4089250d8cd4bbfc62c975efde088c4754d7e6643dea274d590a687be4e',
# 'public_key': '04b42818cba94bafa66759695f66b276c4534cc123aca168239652a493c246fb431c3cfe6aca153b46fa648db1d4fb18e8031641dff09b4a6e91ec830303494d78',
# 'xprivate_key': 'xprv9s21ZrQH143K2SJP6FcFSDsh8dNbVL4C2K4J74bTtXsrvJ57Ybd32q1dJHxBNJajCJVdhXUqiSo579GAR9diAwywZThWHGeRNjRbozqKLuW',
# 'xpublic_key': 'xpub661MyMwAqRbcEvNrCH9FoMpRgfD5tnn3PXytuT15SsQqo6QG68wHadL79Z88gE1Bz4oUX8Gwvs2hSuVVHZxr1XgfZmySmZDb45NkFeAnMgp',
# 'address': '133jabDzv3NJEF9ATuKGFNvv21GPmNWjR5', 'wif': 'L2dmshNAEfp8UKXB4PXK2N7BpnpsFCANYA6S2VzrNVVrvD8tt1oE',
# 'children': [{'private_key': 'ee174b5ec6789da2afb92b459d933349e69c9b27bbace1c18f1fd2f60191aef2',
# 'public_key': '046a8bfd174afd494248e81fb52c816b6c5ee62901f0a4a1f3ad5032f41eb18d26ad2d770e88797aa90f807d36e85a79c171d7bc07dc7b12d496598eae36e18c29',
# 'xpublic_key': 'xpub68454skQiUtf32P5xjJDASD6FffiEJDZfQd6F4ThN8PZ7NzGMUdpqCG4nMxyiH82HqpGunpS6W2XjKtVeztxh1bVRDtgiPvzFarLJ75rKmp',
# 'xprivate_key': 'xprv9u4ifNDWt7LMpYJcrhmCoJGMhdqDpqViJBhVSg45onraEaf7owKaHPwaw5zQDKGmKha6qep7QWUeZ8vW4TBi4T5W9bf5nATxJKiJ2Y5EN6A',
# 'address': '1HdF6fDHMT9cx7NzgsiHyNERmFvGfzE21S', 'segwit': '3QicEA8x1wkkTLGmN1D8J39h2ik4gKPnqi',
# 'wif': 'L5CXcfjbozZCbWh5jbe2aGQkfRuzn4T6enYmx1naYMrqSGBH7hzE', 'path': 'm/0', 'bip32_path': "m/44'/0'/0'/0",
# 'xpublic_key_prime': 'xpub68454skQiUtf32P5xjJDASD6FffiEJDZfQd6F4ThN8PZ7NzGMUdpqCG4nMxyiH82HqpGunpS6W2XjKtVeztxh1bVRDtgiPvzFarLJ75rKmp',
# 'xprivate_key_prime': 'xprv9u4ifNDWt7LMpYJcrhmCoJGMhdqDpqViJBhVSg45onraEaf7owKaHPwaw5zQDKGmKha6qep7QWUeZ8vW4TBi4T5W9bf5nATxJKiJ2Y5EN6A'}],
# 'segwit': '36tRBLwfqJxSVDjusiGoHjZY6X9qgEy21H', 'xpublic_key_prime': 'xpub68454skZ49RdC6p2fRRyp8w6CKDeaeM36kWKj1pNf5vHz4U1QEPHkkBy8L3K1kn7c2iLVALJScTHDbFtgUrm4nRUYbmDc7bGyX5ojNs5xUe',
# 'xprivate_key_prime': 'xprv9u4ifNDfDmsKycjZZPtySzzMeHPABBdBjXaivdQm6kPK7G8rrh53CwsVH3H2DUwHM91se5SnuXtxJag68NPfrSKgno44jcd3nFGEsrL3Ugq'}


# print(create_wallet())
def create_transaction(wallet, wif, amount, coin):
    # Приватный ключ из wif
    my_key = PrivateKey(wif=wif)

    # Коммисия перевода, если поставить слишком маленькую, то транзакцию не примут
    # И чем больше коммисия, тем быстрее пройдет перевод
    fee = 5000

    # Генерация транзакции, тут менять валюту
    coin_hash = my_key.create_transaction([(wallet, amount, f'{coin}')], fee=fee, absolute_fee=True)
    return coin_hash


def check_transaction(coin_hash):
    url = 'https://blockchain.info/pushtx'
    x = requests.post(url, data={'tx': coin_hash})
    result = x.text
    return result


vl, tr = check_wallet_value('1Q2g8fwX2rfG4B4pLoUfnPJPZy4ZQowCcJ')
# print(create_wallet(''))
print(gen_address(0))

# create_transaction(wallet='17ya3bCpPioyPH8kAyFkEDBUqdjF6wwPxo',
#                    wif='L46ixenNSu8Bqk899ZrH8Y96t8DHqJ1ZyxzQBGFTbh38rLHLaPoY', amount=0.1, coin='btc')

key = PrivateKey('L46ixenNSu8Bqk899ZrH8Y96t8DHqJ1ZyxzQBGFTbh38rLHLaPoY')
