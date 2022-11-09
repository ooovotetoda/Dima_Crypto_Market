import requests


# sup
def get_balance():
    r = requests.get('https://nileapi.tronscan.org/api/account/tokens'
                     f'?address=THUv47RmURMHf1ncfVzqig5FUyX8hznU16'
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
