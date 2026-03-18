import requests
import pandas as pd

'''
Enter the url where you data resides. get() is used to fetch data from the url, 
you store it into a variable.'''

url = "https://api.coingecko.com/api/v3/coins/markets"

params = {
    'vs_currency': 'USD',
    'order': 'market_cap_desc',
    'per_page': 10,
    'page': 1
}

response = requests.get(url, params = params)

print(response.status_code)

data = response.json()
print(type(data))
print(data[0])

records = []

for coin in data:

    record = {
        'name': coin.get('name'),
        'symbol': coin.get('symbol'),
        'price': coin.get('current_price'),
        'market_cap': coin.get('market_cap'),
        'circulating_supply': coin.get('circulating_supply'),
        'max_supply': coin.get('max_supply')
    }

    records.append(record)

print(records)

coins = pd.DataFrame(records)

coins['max_supply'] = coins['max_supply'].fillna(0)

coins['price'] = coins['price'].astype('float')
coins['market_cap'] = coins['market_cap'].astype('float')
coins['circulating_supply'] = coins['circulating_supply'].astype('int64')
coins['max_supply'] = coins['max_supply'].astype('int64')

coins.columns = [col.lower() for col in coins.columns]

coins['symbol'] = coins['symbol'].str.upper()

print(coins.tail())

print(coins.dtypes)

print(coins)