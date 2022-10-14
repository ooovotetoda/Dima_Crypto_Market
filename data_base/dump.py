import json
import random

import base58
import ecdsa
import requests
from Crypto.Hash import keccak
from tronpy import Tron
from tronpy.keys import PrivateKey


def keccak256(data):
    hasher = keccak.new(digest_bits=256)
    hasher.update(data)
    return hasher.digest()


def get_signing_key(raw_priv):
    # SigningKey генератор, связанный с определённой кривой. (выбор открытой точки
    # from_string самый короткий формат сериализации SigningKey
    return ecdsa.SigningKey.from_string(raw_priv, curve=ecdsa.SECP256k1)


def verifying_key_to_addr(key):
    pub_key = key.to_string()
    #
    # переводим строку в байты
    primitive_addr = b'\x41' + keccak256(pub_key)[-20:]
    # 0 (zero), O (capital o), I (capital i) and l (lower case L)
    addr = base58.b58encode_check(primitive_addr)
    return addr


API_BASE_URL = 'https://api.shasta.trongrid.io'
MY_PRIV_KEY = '78c93b6ea3df0e48b270f97d948275c3fc7e23d187b464cf26b7a9b9888f3f98'
# hex
FROM_ADDR = '411821a07c8ff1e75f144899e85658d416d2ad0724'
TO_ADDR = "TEiMQZpHs4N4HuTKP3xcCKZ68XSQSfEbMW"
AMOUNT = 1000


# the address must be base58 or hex
def get_balance(address, token_symbol):
    url = "https://apilist.tronscan.org/api/account"
    payload = {
        "address": address,
    }
    res = requests.get(url, params=payload)
    trc20token_balances = json.loads(res.text)["trc20token_balances"]
    print(trc20token_balances)
    token_balance = next((item for item in trc20token_balances if item["symbol"] == token_symbol), None)
    if token_balance is None:
        return 0
    else:
        return int(token_balance["balance"])


def get_transaction_info(owner_address):
    url = "https://api.shasta.trongrid.io/v1/accounts/THtbMw6byXuiFhsRv1o1BQRtzvube9X1jx/transactions?only_confirmed=false&only_unconfirmed=false&only_to=false&only_from=false"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    print(response.text)


def create_transaction():
    url = 'https://api.shasta.trongrid.io/wallet/triggersmartcontract'

    payload = {
        'owner_address': '419adf1f1cd48349087161c262051e7dd589baf2cb',
        'contract_address': '41a7837ce56da0cbb28f30bcd5bff01d4fe7e4c6e3',
        'function_selector': 'transfer(address,uint256)',
        'call_value': 0
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }

    response = requests.post(url, json=payload, headers=headers)

    print(response.text)


def check_transaction_by_hash(hash):
    hash_url = f'https://apilist.tronscanapi.com/api/transaction-info?hash={hash}'
    res = json.loads(requests.get(hash_url).text)
    tokenTransferInfo = res['tokenTransferInfo']
    confirmed, from_address, to_address, amount_str = res['confirmed'], \
                                                      tokenTransferInfo['from_address'], \
                                                      tokenTransferInfo['to_address'], \
                                                      tokenTransferInfo['amount_str']
    return confirmed, from_address, to_address, int(amount_str) / 1000000


# get_account_info('TUismYHRpvEMUjcvjJYttCZbNKjKNzLHuG')

while True:
    # take 32 elements from area [0;256)
    # examples [59, 55, .., 106]
    raw = bytes(random.sample(range(0, 256), 32))
    # raw = bytes.fromhex('a0a7acc6256c3..........b9d7ec23e0e01598d152')
    key = get_signing_key(raw)
    addr = verifying_key_to_addr(key.get_verifying_key()).decode()
    print('Address:     ', addr)
    print('Address(hex):', base58.b58decode_check(addr.encode()).hex())
    print('Public Key:  ', key.get_verifying_key().to_string().hex())
    print('Private Key: ', raw.hex())
    break

HALF_TRON = 500000
ONE_TRON = 1000000

# your wallet information
WALLET_ADDRESS = addr
PRIVATE_KEY = raw.hex()

# connect to the Tron blockchain
client = Tron()


def gen_address():
    url = "https://api.shasta.trongrid.io/wallet/generateaddress"
    headers = {"accept": "application/json"}
    response = requests.get(url, headers=headers)
    print(response.text)


# send some 'amount' of Tron to the 'wallet' address
def send_tron(amount, wallet):
    try:
        priv_key = PrivateKey(bytes.fromhex(PRIVATE_KEY))

        # create transaction and broadcast it
        txn = (
            client.trx.transfer(WALLET_ADDRESS, str(wallet), int(amount))
            .memo("Первая тестовая транза")
            .build()
            .inspect()
            .sign(priv_key)
            .broadcast()
        )
        # wait until the transaction is sent through and then return the details
        return txn.wait()

    # return the exception
    except Exception as ex:
        return ex


# send_tron(1, 'TDgqD6FSsHgdocr9SpZryywL6mjEtqVR2N')
# tronWeb.trx.getTransaction("")
get_transaction_info('41a63aeee03f57ed54ff4fbdc8285563e13d682418')
get_balance('TAqZzenukZdnFdhTxeEtPSEBrD42EKzm3N', 'TRX')
