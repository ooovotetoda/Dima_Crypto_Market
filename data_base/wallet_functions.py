from bipwallet.utils import *
from bipwallet import wallet


def create_wallet():
    # generate 12 word mnemonic seed
    seed = wallet.generate_mnemonic()

    # create bitcoin wallet
    w = wallet.create_wallet(network="BTC", seed=seed, children=1)
    return w

def gen_address(index):
    # Наша seed фраза
    seed = 'during style topic antenna east alien next umbrella mansion bitter dinner merry'

    # Мастер ключ из seed фразы
    master_key = HDPrivateKey.master_key_from_mnemonic(seed)

    # Public key из мастер ключа по пути 'm/44/0/0/0'
    root_keys = HDKey.from_path(master_key, "m/44'/0'/0'/0")[-1].public_key.to_b58check()

    # Extended public key
    xpublic_key = str(root_keys)

    # Адрес дочернего кошелька в зависимости от значения index
    address = Wallet.deserialize(xpublic_key, network='BTC').get_child(index, is_prime=False).to_address()

    rootkeys_wif = HDKey.from_path(master_key, f"m/44'/0'/0'/0/{index}")[-1]

    # Extended private key
    xprivatekey = str(rootkeys_wif.to_b58check())

    # Wallet import format
    wif = Wallet.deserialize(xprivatekey, network='BTC').export_to_wif()

    return address, wif


print(gen_address(0))
print(create_wallet())