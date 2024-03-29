import json
import random

import base58
import ecdsa
import requests
import tronpy.keys
from Crypto.Hash import keccak
from tronpy import Tron
from tronpy.keys import PrivateKey

# client = Tron(HTTPProvider(endpoint_uri='https://api.trongrid.io/', api_key='29d8fee1-28af-4c32-81cb-5f53e5da67b5',))
client = Tron(network='shasta', conf={'fee_limit': 10_000_000, 'timeout': 20.0})
HALF_TRON = 500000
ONE_TRON = 1000000


def gen_address():
    def keccak256(data):
        hasher = keccak.new(digest_bits=256)
        hasher.update(data)
        return hasher.digest()

    def get_signing_key(raw_priv):
        return ecdsa.SigningKey.from_string(raw_priv, curve=ecdsa.SECP256k1)

    def verifying_key_to_addr(key):
        pub_key = key.to_string()
        primitive_addr = b'\x41' + keccak256(pub_key)[-20:]
        # 0 (zero), O (capital o), I (capital i) and l (lower case L)
        addr = base58.b58encode_check(primitive_addr)
        return addr

    while True:
        raw = bytes(random.sample(range(0, 256), 32))
        key = get_signing_key(raw)
        addr = verifying_key_to_addr(key.get_verifying_key()).decode()

        WALLET_ADDRESS = addr
        WALLET_ADDRESS_HEX = base58.b58decode_check(addr.encode()).hex()
        PUBLIC_KEY = key.get_verifying_key().to_string().hex()
        PRIVATE_KEY = raw.hex()

        # print('Address:     ', WALLET_ADDRESS)
        # print('Address(hex):', WALLET_ADDRESS_HEX)
        # print('Public Key:  ', PUBLIC_KEY)
        # print('Private Key: ', PRIVATE_KEY)
        break
    return WALLET_ADDRESS, WALLET_ADDRESS_HEX, PUBLIC_KEY, PRIVATE_KEY


def create_transaction(from_address, to_address, value):
    url = 'https://api.shasta.trongrid.io/wallet/triggersmartcontract'
    payload = {
        'owner_address': f'{from_address}',
        'contract_address': f'{to_address}',
        'function_selector': 'transfer(address,uint256)',
        'call_value': f'{value}'
    }
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json'
    }
    response = requests.post(url, json=payload, headers=headers)
    print(response.text)


# send some 'amount' of Tron to the 'wallet' address
def send_tron(from_wallet, to_wallet, amount):
    try:
        priv_key = PrivateKey(bytes.fromhex('9f0e8cbf8d9f2a2d3ce22983c6af7e8ec1c4545fa71367a3b33e85dd7a669e52'))

        txn = (
            client.trx.transfer("TJzXt1sZautjqXnpjQT4xSCBHNSYgBkDr3", "TVjsyZ7fYF3qLF6BQgPmTEZy1xrNNyVAAA", 1_000)
            .memo("test memo")
            .build()
            .sign(priv_key)
        )
        print(txn.txid)
        print(txn.broadcast().wait())

    # return the exception
    except Exception as ex:
        return ex


# запоминание стоимости товара + get


# the address must be base58 or hex
def get_balance(wallet, net):
    if net == 'TRX':
        try:
            return client.get_account_balance(wallet)
        except tronpy.exceptions.AddressNotFound:
            return 'AccountNotFound'
    elif net == 'USDT':
        r = requests.get('https://nileapi.tronscan.org/api/account/tokens'
                         f'?address={wallet}'
                         '&start=0'
                         '&limit=20'
                         '&token='
                         '&hidden=0'
                         '&show=0'
                         '&sortType=0')
        if r.status_code == 200:
            for token in r.json()['data']:
                if token['tokenAbbr'].lower() == 'usdt':
                    print(token)
                    return token['quantity']
            else:
                return float(0)


def get_trans_by_wallet(wallet, net):
    if net == 'TRX':
        r = requests.get('https://nileapi.tronscan.org/api/transaction'
                         '?sort=-timestamp'
                         '&count=true'
                         '&limit=20'
                         '&start=0'
                         f'&address={wallet}')
        if r.status_code == 200:
            return r.json()
        else:
            return {}
    elif net == 'USDT':
        r = requests.get('https://nileapi.tronscan.org/api/token_trc20/transfers'
                         '?limit=20'
                         '&start=0'
                         '&sort=-timestamp'
                         '&count=true'
                         f'&relatedAddress={wallet}')
        if r.status_code == 200:
            return r.json()
        else:
            return {}



def check_transaction_by_hash(hash):
    hash_url = f'https://apilist.tronscanapi.com/api/transaction-info?hash={hash}'
    res = json.loads(requests.get(hash_url).text)
    tokenTransferInfo = res['tokenTransferInfo']
    confirmed, from_address, to_address, amount_str = res['confirmed'], \
                                                      tokenTransferInfo['from_address'], \
                                                      tokenTransferInfo['to_address'], \
                                                      tokenTransferInfo['amount_str']
    return confirmed, from_address, to_address, int(amount_str) / 1000000


# if __name__ == '__main__':
print(client.to_base58check_address('TK1yi9LxfZ2UFHxVVHi6sjQFxmqrCV5Ene'))
# print(send_tron('TBJpRJvCQFza8GWugJhbvUUaxoTFwEhrDC', 'TDpdD7SsYLHD1FAp888G2RfsSc2EmTXErs', 1))
print(get_balance('TDpdD7SsYLHD1FAp888G2RfsSc2EmTXErs', 'USDT'))
# print(get_trans_by_wallet('TDpdD7SsYLHD1FAp888G2RfsSc2EmTXErs', 'USDT'))
# print(create_transaction('TDgqD6FSsHgdocr9SpZryywL6mjEtqVR2N', 'TEVutcRXu8MDT1UiGYmEJbzVvdz3LudR8a', 0))
# print(get_trans_by_wallet('TEVutcRXu8MDT1UiGYmEJbzVvdz3LudR8a', 'TRX'))
print(tronpy.keys.to_base58check_address('TBJpRJvCQFza8GWugJhbvUUaxoTFwEhrDC'))
# print(client.get_account('TYTaZ9S5uVoVUuU2koSgQaPU3voTWuU6BB'))
# TVUkNF1VFLrzKWnNhSTwQMTMrGXkoRvqw7
# TYTaZ9S5uVoVUuU2koSgQaPU3voTWuU6BB

url = "https://api.shasta.trongrid.io/wallet/createaccount"

payload = {
    "owner_address": "THUv47RmURMHf1ncfVzqig5FUyX8hznU16",
    "account_address": "TBJpRJvCQFza8GWugJhbvUUaxoTFwEhrDC",
    "visible": False
}
headers = {
    "accept": "application/json",
    "content-type": "application/json"
}

response = requests.post(url, json=payload, headers=headers)

print(response.text)