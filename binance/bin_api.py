import requests
from pprint import pprint
import json

hash = '91bd36c32141fea9a6d978e538dc52a7a91788e46331e37d3c8012ac2353905d'
address = ''

adress_url = f'https://apilist.tronscanapi.com/api/transaction?sort=-timestamp&count=true&limit=20&start=0&address={address}'


def check_transaction_by_hash(hash):
    hash_url = f'https://apilist.tronscanapi.com/api/transaction-info?hash={hash}'
    res = json.loads(requests.get(hash_url).text)
    tokenTransferInfo = res['tokenTransferInfo']
    confirmed, from_address, to_address, amount_str = res['confirmed'], \
                                                      tokenTransferInfo['from_address'], \
                                                      tokenTransferInfo['to_address'], \
                                                      tokenTransferInfo['amount_str']
    return confirmed, from_address, to_address, int(amount_str)/1000000


def check_transaction_history_by_adress(address):
    pass


print((check_transaction_by_hash(hash)))
